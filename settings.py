SPECTRUM_BINS = 4096

# button height
BH = 0.05
# button width
BW = 0.07

BUTTONS = {
    'previous': ([0.43, 0.01, BW, BH], 'Prev', '_x_axis_view_prev'),
    'next': ([0.5, 0.01, BW, BH], 'Next', '_x_axis_view_next'),
    "collapse_x": ([0.6, 0.01, BW, BH], 'Collapse x', '_x_axis_collapse_scale'),
    "expand_x": ([0.67, 0.01, BW, BH], 'Expand x', '_x_axis_expand_scale'),
    "collapse_y": ([0.92, 0.3, BW, BH], 'Collapse y', '_y_axis_collapse_scale'),
    "expand_y": ([0.92, 0.35, BW, BH], 'Expand y', '_y_axis_expand_scale'),
    "up": ([0.92, 0.50, BW, BH], 'Up', '_y_axis_view_up'),
    "down": ([0.92, 0.45, BW, BH], 'Down', '_y_axis_view_down'),
    "save": ([0.92, 0.85, BW, BH], 'Save', 'save_svg'),
    "fit_range": ([0.05, 0.01, BW, BH], 'Fit range', '_activate_marking_for_fit'),
    "do_fit": ([0.12, 0.01, BW, BH], 'Fit', 'do_fit'),
    "report_fit": ([0.19, 0.01, BW, BH], 'Report fit', 'report_fit'),
    "mark_peaks": ([0.27, 0.01, BW, BH], 'Mark', '_activate_marking'),
    "save_points": ([0.34, 0.01, BW, BH], 'Report points', 'print_marked_points'),
    "remove": ([0.12, 0.92, BW, BH], 'remove', 'remove_plot'),
    "add_gate": ([0.05, 0.92, BW, BH], 'add', 'add_spectrum_from_file'),
    "show_all": ([0.75, 0.01, BW, BH], 'Show all', 'show_all')
}

TEXT_BOXES = {
    "search_gamma": ([0.92, 0.92, BW, BH], 'Show energy', 0.05, 'show_peak'),
}

RADIO_BUTTONS = {
    "autoscale": ([0.92, 0.6, 0.03, 0.1], ['off', 'on'], 'set_autoscale'),
    "logscale": ([0.96, 0.6, 0.03, 0.1], ['off', 'on'], 'set_logscale')
}

TEXT_FRAMES = {
    "auto": [0.92, 0.71],
    "log": [0.96, 0.71]
}

KEYMAP = {
    'right': '_x_axis_view_next',
    'left': '_x_axis_view_prev',
    'up': '_y_axis_view_up',
    'down': '_y_axis_view_down',
    'ctrl+up': '_y_axis_expand_scale',
    'ctrl+right': '_x_axis_expand_scale',
    'ctrl+left': '_x_axis_collapse_scale',
    'ctrl+down': '_y_axis_collapse_scale',
    'm': '_activate_marking'
}

WINDOW_SETUP = {
    'top': 0.9,
    'bottom': 0.15,
    'left': 0.05,
    'right': 0.91,
    'hspace': 0.2,
    'wspace': 0.2
}

FIGURE_SIZE = (15, 5)
FONTSIZE = 12
BUTTONS_FONTSIZE = 9
LABELS_SIZE = 14

INITIAL_X_AXIS_LIMITS = (0, 500)
SHOW_PEAK_WINDOW_WIDTH = 400

OUTPUT_FIGURES_PATH = 'Output/'
OUTPUT_MARKED_PEAKS_PATH = './Peaks/'
OUTPUT_FIT_RESULTS_PATH = './Fits/'

X_AXIS_MOVING_FACTOR = 0.15
Y_AXIS_MOVING_FACTOR = 0.15
X_AXIS_STRETCH_FACTOR = 5
Y_AXIS_COLLAPSE_SCALE_FACTOR = 1.5
Y_AXIS_EXPAND_SCALE_FACTOR = 0.8

SPECTRUM_PLOT_SETUP = {
    'drawstyle': 'steps-mid',
    'color': None,
    'linestyle': None,
    'linewidth': 1,
    'picker': 10
}

FIT_PLOT_SETUP = {
    'drawstyle': 'default',
    'color': 'red',
    'linestyle': '--',
    'linewidth': 2,
    'picker': 10
}

GATE_NAME_BOX_SETUP = {
    'x': 0.9,
    'y': 0.85,
    'fontsize': 12,
    'horizontalalignment': 'right'
}

DATA_FILETYPES = [
    ('txt', '*.txt'),
    ('hdf5', '*.h5'),
    ('all', '*.*')
]