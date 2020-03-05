import matplotlib.pyplot as plt


class PlotManager:

    def __init__(self, window_object):
        self.window_object = window_object
        self.name_to_line2d = {}
        self.plot_setup = {}

    def add_plot(self, name, data_x, data_y):
        if name in self.name_to_line2d.keys():
            print('The {} keV has been already plotted.'.format(name))
            return None
        else:
            line2d_obj, = self.window_object.ax.plot(
                data_x, data_y, **self.plot_setup
            )
            self.name_to_line2d[name] = line2d_obj
            return line2d_obj

    def remove_plot(self, name):
        try:
            # remove from plot
            self.window_object.ax.lines.remove(self.name_to_line2d[name])
            # remove from PlotManager registry
            del self.name_to_line2d[name]
        except KeyError:
            print('Nothing to remove.')

    def mark_plot(self, name):
        self.name_to_line2d[name].set_linewidth(2)

    @property
    def line2d_to_name(self):
        return {v.__repr__(): k for k, v in self.name_to_line2d.items()}


class ClickCatcher:

    def __init__(self, window_obj):
        print('Marking mode on.')
        self.window = window_obj
        self.window.is_click_catcher_working = True

        self.cid = self.window.fig.canvas.mpl_connect('button_press_event', self)
        self.points = self.initialize_plotting()

        self.cid_key = self.window.fig.canvas.mpl_connect('key_press_event', self.key_press)

        self.data_x = []
        self.data_y = []

    def initialize_plotting(self):
        import settings
        return self.window.ax.plot([], [], **settings.CLICK_CATCHER_PLOT_SETUP)[0]

    def __call__(self, event):
        # ignore toolbar operations like zoom
        state = self.window.fig.canvas.manager.toolbar._active
        if state is not None:
            self.window.fig.canvas.manager.toolbar._active = None
            return None

        # add click catch a new point (add to the list of points)
        if not event.dblclick and event.button == 1 and event.inaxes == self.window.ax:
            self.data_x.append(event.xdata)
            self.data_y.append(event.ydata)
            self.update()
            print('{:8.2f} {:8.2f}'.format(event.xdata, event.ydata))

        # stop click catching points
        elif event.button == 2:
            self.disconnect()

        # cancel previous click
        elif event.button == 3:
            self.data_x.pop()
            self.data_y.pop()
            self.update()
            if not self.data_y:
                self.disconnect()

    def update(self):
        self.points.set_data(self.data_x, self.data_y)
        self.window.fig.canvas.draw()

    def disconnect(self):
        # disconnect click-catching
        self.window.fig.canvas.mpl_disconnect(self.cid)
        # disconnect key bounding
        self.window.fig.canvas.mpl_disconnect(self.cid_key)

        self.window.is_click_catcher_working = False
        self.remove_plot()
        print('Marking mode off.')

    def key_press(self, event):
        if event.key == 'escape':
            self.disconnect()

    def get_data(self):
        return self.data_x, self.data_y

    def remove_plot(self):
        self.points.remove()
        self.window.fig.canvas.draw()


class PeakCatcher(ClickCatcher):

    def initialize_plotting(self):
        import settings
        return self.window.ax.plot([], [], **settings.PEAK_CATCHER_PLOT_SETUP)[0]


class SpectrumSelector:

    def __init__(self, window_obj):
        self.window = window_obj
        self.cid = self.window.fig.canvas.mpl_connect('pick_event', self)

        self._selected_spectrum = None
        self._is_highlighted = False

    def __call__(self, event):
        if self.window.is_click_catcher_working:
            pass
        else:
            self.selected_spectrum = event.artist
            plt.draw()

    def set_non_event_selection(self, line2d_obj):
        # for auto selection when spectrum is added to the plot
        self.selected_spectrum = line2d_obj
        self.selected_spectrum.set_linewidth(1)

    @property
    def selected_spectrum(self):
        return self._selected_spectrum

    @selected_spectrum.setter
    def selected_spectrum(self, new_spectrum):
        if self._selected_spectrum == new_spectrum and not self._is_highlighted:
            self._is_highlighted = True
            self._selected_spectrum.set_linewidth(2)

        elif self._selected_spectrum == new_spectrum and self._is_highlighted:
            self._is_highlighted = False
            self._selected_spectrum.set_linewidth(1)

        elif self._is_highlighted != new_spectrum:
            if self.selected_spectrum:
                self._selected_spectrum.set_linewidth(1)
            self._selected_spectrum = new_spectrum
            self._selected_spectrum.set_linewidth(2)

        self.window.selected_spectrum = self.selected_spectrum
