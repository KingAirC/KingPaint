from ..geometry.king_plane_geometry_graph import KingPoint
from ..core.king_decorater import geometry_generate
from ..core.king_figure import KingFigure


@geometry_generate(cls=KingPoint)
def _point_on_curve(depends=(), essential_data=None):
    curve = depends[0]
    x_data = curve.get_xdata()
    y_data = curve.get_ydata()
    essential_data = essential_data % len(x_data)
    return [x_data[essential_data], y_data[essential_data]]


def get_manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def get_min_manhattan_distance_index_by_point_xy_data(x, y, x_data, y_data, i_from, i_range):
    index = None
    dis = None
    length = len(x_data)
    i_min = i_from - i_range
    i_max = i_from + i_range
    j = i_min
    while j < i_max:
        j2 = j % length
        new_dis = get_manhattan_distance(x, y, x_data[j2], y_data[j2])
        if dis is None:
            dis = new_dis
            index = j2
        else:
            if new_dis < dis:
                dis = new_dis
                index = j2
        j += 1
    return index


def get_index_by_curve_mouse(i, curve, delta_x, delta_y, new_x, new_y):
    x_data = curve.get_xdata()
    y_data = curve.get_ydata()
    length = len(x_data)
    i_range = 10 + int(abs((delta_x + delta_y) * 100))
    if i_range > length:
        i_range = length
    return get_min_manhattan_distance_index_by_point_xy_data(new_x, new_y, x_data, y_data, i, i_range)


def get_init_index(x_data, y_data, x_min=None, x_max=None, y_min=None, y_max=None):
    x_min_fig, x_max_fig = KingFigure().get_x_lim()
    y_min_fig, y_max_fig = KingFigure().get_y_lim()
    if x_min is None:
        x_min = x_min_fig
    if x_max is None:
        x_max = x_max_fig
    if y_min is None:
        y_min = y_min_fig
    if y_max is None:
        y_max = y_max_fig
    for i in range(len(x_data)):
        if x_min < x_data[i] < x_max and y_min < y_data[i] < y_max:
            return i
    return 0


def point_on_curve(curve, x_min=None, x_max=None, y_min=None, y_max=None):
    x_data = curve.get_xdata()
    y_data = curve.get_ydata()
    mouse_loc = get_init_index(x_data, y_data, x_min, x_max, y_min, y_max)
    res = _point_on_curve(depends=[curve], essential_data=mouse_loc)
    res.mouse_translation = True

    def new_calc_essential_data_by_delta(delta, new_data):
        ind = get_index_by_curve_mouse(res.essential_data, curve, delta[0], delta[1], new_data[0], new_data[1])
        return ind

    res.calc_essential_data_by_delta = new_calc_essential_data_by_delta

    return res
