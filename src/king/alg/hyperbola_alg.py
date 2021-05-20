from .basic_alg import linspace, sqrt, nan
from .plane_geometry_alg import get_transform_vector_to_y_up


def get_hyperbola_focus_diff_by_standard_equation(a11, a12, a22, a1, a2, a0):
    """
    a11 = (+/-) 1/a^2
    a22 = (+-) 1/b^2
    a12 = a1 = a2 = 0
    a0 = (+-) 1
    """
    if a11 < 0:
        a11 = -a11
        a22 = -a22
        a0 = -a0
    if a0 > 0:
        a11_1 = 1 / a11
        cc = a11_1 - 1 / a22
        a = sqrt(a11_1)
        c = sqrt(cc)
        return [[c, 0], [-c, 0], 2 * a]
    a22_1 = 1 / a22
    cc = 1 / a11 - a22_1
    b = sqrt(-a22_1)
    c = sqrt(cc)
    return [[0, c], [0, -c], 2 * b]


def get_hyperbola_equation_coefficient_by_simplest_focus_diff(x1, y1, x2, y2, diff):
    """
    [1/a^2, 0, -1/b^2, 0, 0, (+-) 1]
    """
    if y1 == 0:
        c = abs(x1)
        cc = c ** 2
        a = diff / 2
        aa = a ** 2
        bb = cc - aa
        return [1 / aa, 0, -1 / bb, 0, 0, -1]
    c = abs(y1)
    cc = c ** 2
    b = diff / 2
    bb = b ** 2
    aa = cc - bb
    return [1 / aa, 0, -1 / bb, 0, 0, 1]


def get_hyperbola_xy_data_by_standard_equation(a11, a12, a22, a1, a2, a0, x_min, x_max, y_min, y_max):
    if a11 < 0:
        a11 = -a11
        a22 = -a22
        a0 = -a0
    if a0 > 0:
        x = linspace(x_min, x_max, 300)
        b = 1 / sqrt(-a22)
        y = b * sqrt(1 + x ** 2 * a11)
        result_x = []
        result_y = []
        result_x.extend(x)
        result_x.append(nan)
        result_x.extend(x)
        result_y.extend(y)
        result_y.append(nan)
        result_y.extend(-y)
        return [result_x, result_y]
    y = linspace(y_min, y_max, 300)
    a = 1 / sqrt(a11)
    x = a * sqrt(1 - y ** 2 * a22)
    result_x = []
    result_y = []
    result_x.extend(x)
    result_x.append(nan)
    result_x.extend(-x)
    result_y.extend(y)
    result_y.append(nan)
    result_y.extend(y)
    return [result_x, result_y]


def get_hyperbola_xy_data_by_simplest_focus_diff(x1, y1, x2, y2, diff, x_min, x_max, y_min, y_max):
    return get_hyperbola_xy_data_by_standard_equation(
        *get_hyperbola_equation_coefficient_by_simplest_focus_diff(x1, y1, x2, y2, diff), x_min, x_max, y_min, y_max)


def get_hyperbola_xy_data_by_focus_diff(x1, y1, x2, y2, diff, x_min, x_max, y_min, y_max):
    """
    get hyperbola point set by two focus, difference, x limit and y limit.
    return : tow set represent for tow line.
    """
    b = abs(diff) / 2
    b_2 = b ** 2
    c2_2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
    c_2 = c2_2 / 4
    a_2 = c_2 - b_2
    if c_2 <= b_2:
        raise Exception("Can not plot a hyperbola")

    def line_func(x):
        return b * sqrt(1 + x ** 2 / a_2)

    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    x_lim = x_max - x_min
    t1, t2 = get_transform_vector_to_y_up(x1, y1, x2, y2)
    center_x_new, center_y_new = t2(center_x, center_y)
    x_lim_new = 0.71 * x_lim
    x_set = linspace(center_x_new - x_lim_new, center_x_new + x_lim_new, 300)
    y_set_1 = line_func(x_set)
    y_set_2 = -y_set_1
    result_1 = t1(x_set, y_set_1)
    result_2 = t1(x_set, y_set_2)

    x_data = []
    x_data.extend(result_1[0])
    x_data.append(nan)
    x_data.extend(result_2[0])
    y_data = []
    y_data.extend(result_1[1])
    y_data.append(nan)
    y_data.extend(result_2[1])

    return [x_data, y_data]
