import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox, RadioButtons
import os
import tkinter as tk
from tkinter import filedialog

from plot_utils import ClickCatcher, SpectrumSelector, PeakCatcher, PlotManager
from datatypes import DataSet
from peak_fitter import PeakFitter, Peak
import settings


class Window:

    BUTTONS_DICT = settings.BUTTONS
    TEXT_BOXES_DICT = settings.TEXT_BOXES
    RADIO_BUTTONS = settings.RADIO_BUTTONS
    KEYMAP = settings.KEYMAP

    def __init__(self):
        self.bins = settings.SPECTRUM_BINS
        self.is_autoscale_on = False
        self.is_click_catcher_working = False
        self.click_data = None
        self.fit_click = None
        self.click_data_for_fit = None
        self.peak_fit = None

        self.fig, self.ax = plt.subplots()
        self.configure_appearance()
        self.configure_behaviour()

        self._add_buttons()
        self._add_text_boxes()
        self._add_check_buttons()
        self._add_text_frames()
        self.fig.canvas.mpl_connect('key_press_event', self._key_press)

        self.selection = SpectrumSelector(self)
        self.spect_plot_manager = PlotManager(self)
        self.spect_plot_manager.plot_setup = settings.SPECTRUM_PLOT_SETUP
        self.fit_plot_manager = PlotManager(self)
        self.fit_plot_manager.plot_setup = settings.FIT_PLOT_SETUP

        self._selected_spectrum = None
        self._gate_name = ''

        self.gate_name_box = plt.gcf().text(
            s=self.gate_name, **settings.GATE_NAME_BOX_SETUP
        )

        plt.show()

    @classmethod
    def add_new_window(cls, event):
        return cls()

    @property
    def gate_name(self):
        return self._gate_name

    @gate_name.setter
    def gate_name(self, value):
        # update gate name text box
        self.gate_name_box.set_text(f'{value}')
        if value:
            self.gate_name_box.set_c(self.selected_spectrum.get_c())
        self._gate_name = value

    @property
    def selected_spectrum(self):
        return self._selected_spectrum

    @selected_spectrum.setter
    def selected_spectrum(self, value):
        self._selected_spectrum = value

        # setting current spectrum name (self.gaten_name)
        if value:
            try:
                self.gate_name = self.spect_plot_manager.line2d_to_name[value.__repr__()]
            except KeyError:
                self.gate_name = self.fit_plot_manager.line2d_to_name[value.__repr__()]
        else:
            self.gate_name = ''
        self._update_plot()

    def catch_coordinates(self):
        click = ClickCatcher(self)
        self.click_data = click.get_data()

    def activate_marking(self, event):
        if self.is_click_catcher_working:
            pass
        else:
            self.is_click_catcher_working = True
            self.catch_coordinates()

    def catch_points_for_fitting(self):
        self.fit_click = PeakCatcher(self)
        self.click_data_for_fit = self.fit_click.get_data()

    def do_fit(self, event):
        # read selected main points for fit
        try:
            fit_peaks = [
                Peak(cen, amp) for cen, amp in zip(
                    self.click_data_for_fit[0][1:-1],
                    self.click_data_for_fit[1][1:-1]
                )
            ]

            # read fit x range
            fit_range = [
                int(self.click_data_for_fit[0][0]),
                int(self.click_data_for_fit[0][-1])
            ]

            # read data for fit in selected range
            data_x, data_y = self.selected_spectrum.get_data()
            data_x = data_x[slice(*fit_range)]
            data_y = data_y[slice(*fit_range)]

            # calculate fit
            self.peak_fit = PeakFitter(data_x=data_x, data_y=data_y, peaks=fit_peaks)
            self.peak_fit.do_fit(verbosity=settings.FIT_VERBOSITY)
            result_x, result_y = self.peak_fit.get_result()

            # plot fit result
            self.fit_plot_manager.add_plot(
                f'fit_{PeakFitter.ith_fit}_{self.gate_name}', result_x, result_y
            )

            # disconnect catching points for fit
            self.fit_click.disconnect()

            self._update_plot()

        except (TypeError, ValueError, AttributeError):
            print('No data for fit.')

    def activate_marking_for_fit(self, event):
        if self.is_click_catcher_working:
            pass
        else:
            self.is_click_catcher_working = True
            self.catch_points_for_fitting()

    def report_fit(self, event):
        gate_name = self.gate_name.replace(' ', '')
        file_name = f'fit_results_{gate_name}.txt'
        file_path = settings.OUTPUT_FIT_RESULTS_PATH
        file = os.path.join(file_path, file_name)

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        report = self.peak_fit.generate_fit_report()
        with open(file, 'a') as f:
            f.write(report)

    def print_marked_points(self, event):
        try:
            result = self.get_clicked_points()
            gate_name = self.gate_name.replace(' ', '')
            file_name = f'peaks_{gate_name}.csv'
            file_path = settings.OUTPUT_MARKED_PEAKS_PATH
            file = os.path.join(file_path, file_name)

            if not os.path.exists(file_path):
                os.makedirs(file_path)

            with open(file, 'a') as f:
                f.write('E [keV], N\n')
                f.write(result)

            print(f'Marked points saved to the {file} file.')

        except TypeError:
            # when no data was selected
            print('There aren\'t any marked points.')

    def get_clicked_points(self):
        output = '{:.2f}, {:.2f}\n'*len(self.click_data[0])
        xy_pairs = list(zip(*self.click_data))
        flat_list = [item for sublist in xy_pairs for item in sublist]
        return output.format(*flat_list)

    def configure_behaviour(self):
        # deactivate the default keymap
        cid_default = self.fig.canvas.manager.key_press_handler_id
        self.fig.canvas.mpl_disconnect(cid_default)

    def configure_appearance(self):
        plt.subplots_adjust(**settings.WINDOW_SETUP)
        self.fig.canvas.set_window_title('Spcetview')
        self.fig.set_size_inches(*settings.FIGURE_SIZE)
        self.ax.tick_params(axis='both', labelsize=settings.LABELS_SIZE)
        self.ax.set_ylabel('Number of counts', fontsize=settings.LABELS_SIZE)
        self.ax.set_xlim(*settings.INITIAL_X_AXIS_LIMITS)

    def _update_plot(self):
        if self.is_autoscale_on:
            self._y_axis_autoscale()
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
        file_path = filedialog.askopenfilename(filetypes=settings.DATA_FILETYPES)
        print(f'{file_path} file opened.')
        return file_path

    def add_spectrum_from_file(self, event):
        file_path = Window.open_file_dialog()

        if file_path:
            dataset = Window.load_data_from_file(filename=file_path)
            line2d = self.spect_plot_manager.add_plot(
                name=dataset.gate.__repr__(),
                data_x=dataset.get_spectrum()[0],
                data_y=dataset.get_spectrum()[1]
            )

            # auto-select the new spectrum
            self.selected_spectrum = line2d
            self.ax.relim()
            self._update_plot()

    def auto_select_next_plot(self):
        # auto-select another spectrum if there still is another plot
        if self.spect_plot_manager.name_to_line2d:
            self.selected_spectrum = (
                next(iter(self.spect_plot_manager.name_to_line2d.values()))
            )
        else:
            self.selected_spectrum = None

    def remove_plot(self, event):
        try:
            # remove selected spectrum plot
            self.spect_plot_manager.remove_plot(self.gate_name)

            # clear fit plots which belong to removed spectrum
            for name in self.fit_plot_manager.line2d_to_name.values():
                if name.endswith(self.gate_name):
                    self.fit_plot_manager.remove_plot(name)

            # auto-select another spectrum if there still is another plot
            self.auto_select_next_plot()

        except KeyError:
            # key error occurs when selected line was the fit_plot_manager object
            # not spect_plot_manager object
            self.fit_plot_manager.remove_plot(self.gate_name)
            self.selected_spectrum = None
            # auto-select another spectrum if there still is another plot
            self.auto_select_next_plot()

        except ValueError:
            print("Nothing to clear.")

    def show_peak(self, text):
        peak = eval(text)
        d = int(settings.SHOW_PEAK_WINDOW_WIDTH/2)
        try:
            self.ax.set_xlim(peak - d, peak + d)
        except:
            print('Incorrect energy.')
        self._y_axis_autoscale()
        self._update_plot()

    def save_svg(self, event):
        filename = "{}_{}-{}.svg".format(
            self.gate_name.replace(' ', ''),
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
            self.is_autoscale_on = False
        self._update_plot()
        print(f'Y autoscale set {label}')

    def set_logscale(self, label):
        if label == 'on':
            self.ax.set_yscale('log')
        else:
            self.ax.set_yscale('linear')
        self._update_plot()
        print(f'Y log set {label}')

    def _y_axis_autoscale(self):
        try:
            x1, x2 = self.ax.get_xlim()
            x1, x2 = max(0, x1), min(x2, self.bins)
            data_y = self.selected_spectrum.get_data(orig=True)[1]
            spect_slice = data_y[int(x1): int(x2)]
            self.ax.set_ylim(0, 1.2 * max(spect_slice))

        except (ValueError, AttributeError) as error:
            print(f'{error}. You can\'t use autoscale now.')
            self.rbutton_name_autoscale.set_active(0)

    def show_all(self, event):
        try:
            x1, *_, x2 = self.selected_spectrum.get_data(orig=True)[0]
            self.ax.set_xlim(x1, x2)
            self._y_axis_autoscale()
        except AttributeError:
            # if there is no spectrum just do nothing
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

    def x_axis_view_next(self, event):
        start, end = self.ax.get_xlim()
        step = self.x_axis_step
        self.ax.set_xlim(start + step, end + step)
        self._update_plot()

    def x_axis_view_prev(self, event):
        start, end = self.ax.get_xlim()
        step = self.x_axis_step
        self.ax.set_xlim(start - step, end - step)
        self._update_plot()

    def y_axis_view_up(self, event):
        start, end = self.ax.get_ylim()
        step = self.y_axis_step
        self.ax.set_ylim(start + step, end + step)
        self._update_plot()

    def y_axis_view_down(self, event):
        start, end = self.ax.get_ylim()
        step = self.y_axis_step
        self.ax.set_ylim(start - step, end - step)
        self._update_plot()

    def x_axis_expand_scale(self, event):
        stretch_width = settings.X_AXIS_STRETCH_FACTOR
        x1, x2 = self.ax.get_xlim()
        self.ax.set_xlim(x1+stretch_width, x2-stretch_width)
        self._update_plot()

    def x_axis_collapse_scale(self, event):
        stretch_width = settings.X_AXIS_STRETCH_FACTOR
        x1, y2 = self.ax.get_xlim()
        self.ax.set_xlim(x1-stretch_width, y2+stretch_width)
        self._update_plot()

    def y_axis_expand_scale(self, event):
        expand_factor = settings.Y_AXIS_EXPAND_SCALE_FACTOR
        y1, y2 = self.ax.get_ylim()
        self.ax.set_ylim(y1, expand_factor*y2)
        self._update_plot()

    def y_axis_collapse_scale(self, event):
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

    def _add_text_frames(self):
        # plt.gcf() let us use figure coordinates instead of axis coordinates
        for text, coords in settings.TEXT_FRAMES.items():
            plt.gcf().text(*coords, text, fontsize=settings.BUTTONS_FONTSIZE)


if __name__ == '__main__':

    win = Window()

