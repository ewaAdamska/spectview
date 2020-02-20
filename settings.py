

# button height
BH = 0.05
# button width
BW = 0.07

BUTTONS = {
    'previous': ([0.43, 0.01, BW, BH], 'Prev', '_x_axis_view_prev'),
    'next': ([0.5, 0.01, BW, BH], 'Next', '_x_axis_view_next'),
    "collapse_x": ([0.6, 0.01, BW, BH], 'Collapse x', '_x_axis_collapse_scale'),
    "expand_x": ([0.67, 0.01, BW, BH], 'Expand x', '_x_axis_expand_scale'),
    "collapse_y": ([0.91, 0.26, BW, BH], 'Collapse y', '_y_axis_collapse_scale'),
    "expand_y": ([0.91, 0.335, BW, BH], 'Expand y', '_y_axis_expand_scale'),
    "up": ([0.91, 0.50, BW, BH], 'Up', '_y_axis_view_up'),
    "down": ([0.91, 0.4, BW, BH], 'Down', '_y_axis_view_down'),
    "save": ([0.91, 0.8, BW, BH], 'Save', 'save_svg'),
    "fit_range": ([0.05, 0.01, BW, BH], 'Fit range', '_activate_marking_for_fit'),
    # "fit_peaks": ([0.12, 0.01, BW, BH], 'Fit peaks', '_activate_marking'),
    "do_fit": ([0.19, 0.01, BW, BH], 'Fit', 'do_fit'),
    "mark_peaks": ([0.27, 0.01, BW, BH], 'Mark', '_activate_marking'),
    "save_points": ([0.34, 0.01, BW, BH], 'Print', 'print_marked_points'),
    "remove": ([0.2, 0.9, BW, BH], 'remove', 'remove_plot'),
    "add_gate": ([0.05, 0.9, BW, BH], 'add', 'add_spectrum_from_file')
}

TEXT_BOXES = {
    "search_gamma": ([0.6, 0.9, 0.075, 0.075], 'Energy', 0.05, 'show_peak'),
}

RADIO_BUTTONS = {
    "autoscale": ([0.91, 0.6, 0.075, 0.1], ['off', 'on'], 'set_autoscale')
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

FIGURE_SIZE = (15, 5)
FONTSIZE = 12
BUTTONS_FONTSIZE = 9
LABELS_SIZE = 14

INITIAL_X_AXIS_LIMITS = (0, 500)

GATE_BOX_HEIGHT_FACTOR = 0.1
GATE_BOX_WIDTH_FACTOR = 0.2
GATE_BOX_X_POSITION_FACTOR = 0.75
GATE_BOX_Y_POSITION_FACTOR = 1.1

OUTPUT_FIGURES_PATH = 'Output/'

X_AXIS_MOVING_FACTOR = 0.15
Y_AXIS_MOVING_FACTOR = 0.15
X_AXIS_STRETCH_FACTOR = 5
Y_AXIS_COLLAPSE_SCALE_FACTOR = 1.5
Y_AXIS_EXPAND_SCALE_FACTOR = 0.8