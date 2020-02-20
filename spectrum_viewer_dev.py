import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, RadioButtons
import os
import tkinter as tk
from tkinter import filedialog

from plot_utils import ClickCatcher, SpectrumSelector, PeakCatcher
from datatypes import DataSet
from peak_fitter import PeakFitter, Peak
import settings


class PlotManager:

    def __init__(self, window_object):
        self.window_object = window_object
        self._gate_name_to_line2d = {}
        self._gate_name_to_data_set = {}

    def add_plot(self, gate_name, data_x, data_y):
        if gate_name in self._gate_name_to_line2d.keys():
            print('The {} was already plotted.'.format(gate_name))
            return None
        else:
            line2d_obj = self.window_object.ax.plot(data_x, data_y, drawstyle='steps-mid', lw=1, picker=10)
            line2d_obj = line2d_obj[0]
            self._gate_name_to_line2d[gate_name] = line2d_obj
            return line2d_obj

    def remove_plot(self, gate_name):
        self.window_object.ax.lines.remove(self._gate_name_to_line2d[gate_name])

    def mark_plot(self, gate_name):
        self._gate_name_to_line2d[gate_name].set_linewidth(2)

    @property
    def line2d_to_gate_name(self):
        return {v.__repr__(): k for k, v in self._gate_name_to_line2d.items()}


class Window:

    BUTTONS_DICT = settings.BUTTONS
    TEXT_BOXES_DICT = settings.TEXT_BOXES
    RADIO_BUTTONS = settings.RADIO_BUTTONS
    KEYMAP = settings.KEYMAP

    def __init__(self):
        self.bins = 4096
        self.is_autoscale_on = False
        self.is_click_catcher_working = False
        self.click_data = ([], [])

        self.fig, self.ax = plt.subplots()
        self.configure_appearance()

        self._add_buttons()
        self._add_text_boxes()
        self._add_check_buttons()
        self.fig.canvas.mpl_connect('key_press_event', self._key_press)

        self.selection = SpectrumSelector(self)
        self.plot_manager = PlotManager(self)

        self.fit_plots = []

        self._selected_spectrum = None
        self._gate_name = ''
        self.gate_name_box = self.ax.text(
            self.ax.get_xlim()[1] - 1.1 * self.gate_box_width,
            self.ax.get_ylim()[1] - 1.1 * self.gate_box_height,
            "{}".format(self._gate_name),
            fontsize=settings.FONTSIZE
        )

    @property
    def selected_spectrum(self):
        return self._selected_spectrum

    @selected_spectrum.setter
    def selected_spectrum(self, value):
        if value:
            self._gate_name = self.plot_manager.line2d_to_gate_name[value.__repr__()]
        else:
            self._gate_name = ''
        self.gate_name_box.set_text("{}".format(self._gate_name))
        self._selected_spectrum = value
        self._update_plot()

    def catch_coordinates(self):

        click = ClickCatcher(self)
        self.click_data = click.get_data()

    def _activate_marking(self, event):
        if self.is_click_catcher_working:
            pass
        else:
            self.is_click_catcher_working = True
            self.catch_coordinates()



    def catch_points_for_fitting(self):
        click = PeakCatcher(self)
        self.click_data_for_fit = click.get_data()


    def do_fit(self, event):
        print(self.click_data_for_fit)
        fit_peaks = [Peak(cen, amp) for cen, amp in zip(self.click_data_for_fit[0][1:-1], self.click_data_for_fit[1][1:-1])]
        fit_range = [int(self.click_data_for_fit[0][0]), int(self.click_data_for_fit[0][-1])]
        print(f'range {fit_range} and peaks:\n{fit_peaks}')

        data_x, data_y = self.selected_spectrum.get_data()
        data_x = data_x[fit_range[0]: fit_range[1]]
        data_y = data_y[fit_range[0]: fit_range[1]]

        peak_fit = PeakFitter(data_x=data_x, data_y=data_y, peaks=fit_peaks)
        peak_fit.fit_all()
        result_x, result_y = peak_fit.get_result()

        plot = self.ax.plot(result_x, result_y, 'r-', label='best fit')
        plot = plot[0]
        self.fit_plots.append(plot)
        plt.draw() #TODO: removing plot

    def _activate_marking_for_fit(self, event):
        if self.is_click_catcher_working:
            pass
        else:
            self.is_click_catcher_working = True
            self.catch_points_for_fitting()


    def print_marked_points(self, event):
        self.print_points()

    def print_points(self):
        output = '({:.2f}, {:.2f}) ; '*len(self.click_data[0])
        xy_pairs = list(zip(*self.click_data))
        flat_list = [item for sublist in xy_pairs for item in sublist]
        print(output.format(*flat_list))

    def configure_appearance(self):
        self.fig.set_size_inches(*settings.FIGURE_SIZE)
        self.ax.tick_params(axis='both', labelsize=settings.LABELS_SIZE)
        # self.ax.set_xlabel('Energy (keV)', fontsize=settings.FONTSIZE)
        self.ax.set_ylabel('Number of counts', fontsize=settings.FONTSIZE)
        plt.subplots_adjust(bottom=0.15, left=0.1)
        self.ax.set_xlim(*settings.INITIAL_X_AXIS_LIMITS)

    @property
    def gate_box_height(self):
        factor = settings.GATE_BOX_HEIGHT_FACTOR
        return factor * (self.ax.get_ylim()[1] - self.ax.get_ylim()[0])

    @property
    def gate_box_width(self):
        factor = settings.GATE_BOX_WIDTH_FACTOR
        return factor * (self.ax.get_xlim()[1] - self.ax.get_xlim()[0])

    def _update_plot(self):
        if self.is_autoscale_on:
            self._y_axis_autoscale()
        self.gate_name_box.set_position(
            [self.ax.get_xlim()[1] - settings.GATE_BOX_X_POSITION_FACTOR * self.gate_box_width,
             self.ax.get_ylim()[1] - settings.GATE_BOX_Y_POSITION_FACTOR * self.gate_box_height]
        )

        plt.draw()

    @staticmethod
    def load_data_from_file(filename):
        if filename.endswith('.txt'):
            return DataSet.from_txt(file=filename)
        elif filename.endswith('.h5'):
            return DataSet.from_hdf5(file=filename)
        else:
            print('Wrong data file extension.')
            return None

    @staticmethod
    def open_file_dialog():
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        print(f'{file_path} file opened.')
        return file_path

    def add_spectrum_from_file(self, event):
        file_path = Window.open_file_dialog()
        if file_path:
            dataset = Window.load_data_from_file(filename=file_path)
            line2d = self.plot_manager.add_plot(
                gate_name=dataset.gate.__repr__(),
                data_x=dataset.get_spectrum()[0],
                data_y=dataset.get_spectrum()[1]
            )
            self.selection.set_non_event_selection(line2d_obj=line2d)
            self.ax.relim()
            self._update_plot()

    def remove_plot(self, event):
        try:
            self.ax.lines.remove(self.selected_spectrum)
            self.selected_spectrum = None

            #clear fit plots
            for line in self.fit_plots:
                self.ax.lines.remove(line)

        except ValueError:
            print("Nothing to clear.")

    def show_peak(self, text):
        peak = eval(text)
        try:
            self.ax.set_xlim(peak - 200, peak + 200)

        except:
            print('Incorrect energy.')
        self._y_axis_autoscale()
        self._update_plot()

    def save_svg(self, event):
        filename = "{}_{}-{}.svg".format(
            self._gate_name.replace(' ', ''),
            int(self.ax.get_xlim()[0]),
            int(self.ax.get_xlim()[1])
        )
        if not os.path.exists(settings.OUTPUT_FIGURES_PATH):
            os.makedirs(settings.OUTPUT_FIGURES_PATH)

        plt.savefig(os.path.join(settings.OUTPUT_FIGURES_PATH, filename))

        print('File {} saved.'.format(filename))

    def set_autoscale(self, label):
        if label == 'on':
            self.is_autoscale_on = True
        else:
            self.is_autoscale_on = False
        self._update_plot()
        print('Y autoscale set {}'.format(label))


    def _y_axis_autoscale(self):
        try:
            x1, x2 = self.ax.get_xlim()
            x1, x2 = max(0, x1), min(x2, self.bins)
            data_y = self.selected_spectrum.get_data(orig=True)[1]
            spect_slice = data_y[int(x1): int(x2)]
            self.ax.set_ylim(0, 1.2 * max(spect_slice))
        except (ValueError, AttributeError):
            self.rbutton_name_autoscale.set_active(0) # TODO: maybe put it in some other place
            pass

    @staticmethod
    def do_nothing(event):
        print('Nothing done!')

    @property
    def x_axis_step(self):
        return settings.X_AXIS_MOVING_FACTOR * (self.ax.get_xlim()[1] - self.ax.get_xlim()[0])

    @property
    def y_axis_step(self):
        return settings.Y_AXIS_MOVING_FACTOR * (self.ax.get_ylim()[1] - self.ax.get_ylim()[0])

    def _x_axis_view_next(self, event):
        start, end = self.ax.get_xlim()
        step = self.x_axis_step
        self.ax.set_xlim(start + step, end + step)
        self._update_plot()

    def _x_axis_view_prev(self, event):
        start, end = self.ax.get_xlim()
        step = self.x_axis_step
        self.ax.set_xlim(start - step, end - step)
        self._update_plot()

    def _y_axis_view_up(self, event):
        start, end = self.ax.get_ylim()
        step = self.y_axis_step
        self.ax.set_ylim(start + step, end + step)
        self._update_plot()

    def _y_axis_view_down(self, event):
        start, end = self.ax.get_ylim()
        step = self.y_axis_step
        self.ax.set_ylim(start - step, end - step)
        self._update_plot()

    def _x_axis_expand_scale(self, event):
        stretch_width = settings.X_AXIS_STRETCH_FACTOR
        x1, x2 = self.ax.get_xlim()
        self.ax.set_xlim(x1+stretch_width, x2-stretch_width)
        self._update_plot()

    def _x_axis_collapse_scale(self, event):
        stretch_width = settings.X_AXIS_STRETCH_FACTOR
        x1, y2 = self.ax.get_xlim()
        self.ax.set_xlim(x1-stretch_width, y2+stretch_width)
        self._update_plot()

    def _y_axis_expand_scale(self, event):
        expand_factor = settings.Y_AXIS_EXPAND_SCALE_FACTOR
        y1, y2 = self.ax.get_ylim()
        self.ax.set_ylim(y1, expand_factor*y2)
        self._update_plot()

    def _y_axis_collapse_scale(self, event):
        collapse_factor = settings.Y_AXIS_COLLAPSE_SCALE_FACTOR
        y1, y2 = self.ax.get_ylim()
        self.ax.set_ylim(y1, collapse_factor*y2)
        self._update_plot()

    def _add_buttons(self):
        for key, item in Window.BUTTONS_DICT.items():
            button_name = 'button_{}'.format(key)
            setattr(self, button_name, Button(plt.axes(item[0]), item[1]))
            getattr(self, button_name).on_clicked(getattr(self, item[2]))
            getattr(self, button_name).label.set_fontsize(settings.BUTTONS_FONTSIZE)

    def _add_text_boxes(self):
        for key, item in Window.TEXT_BOXES_DICT.items():
            tbox_name = 'tbox_{}'.format(key)
            setattr(self, tbox_name, TextBox(plt.axes(item[0]), item[1], '', label_pad=item[2]))
            getattr(self, tbox_name).on_submit(getattr(self, item[3]))

    def _add_check_buttons(self):
        for key, item in Window.RADIO_BUTTONS.items():
            rbutton_name = 'rbutton_name_{}'.format(key)
            setattr(self, rbutton_name, RadioButtons(plt.axes(item[0]), item[1]))
            getattr(self, rbutton_name).on_clicked(getattr(self, item[2]))

    def _key_press(self, event):
        for key, _function in Window.KEYMAP.items():
            if event.key == key:
                getattr(self, _function)(event)


if __name__ == '__main__':

    win = Window()
    plt.show()

