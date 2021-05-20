from .basic_alg import linspace
from .plane_geometry_alg import get_distance_by_tow_point, get_transform_vector_to_y_up


def get_parabola_focus_by_standard_equation(a11, a12, a22, a1, a2, a0):
    if a11 == 0:
        return [-a1 / 2, 0]
    return [0, -a2 / 2]


def get_parabola_equation_coefficient_by_simplest_focus(xp, yp):
    if yp == 0:
        return [0, 0, 1, -2 * xp, 0, 0]
    return [1, 0, 0, 0, -2 * yp, 0]


def get_parabola_xy_data_by_standard_equation(a11, a12, a22, a1, a2, a0, x_min, x_max, y_min, y_max):
    if a22 == 0:
        x = linspace(x_min, x_max, 300)
        y = -a11 * x ** 2 / (2 * a2)
        return [x, y]
    y = linspace(y_min, y_max, 300)
    x = -a22 * y ** 2 / (2 * a1)
    return [x, y]


def get_parabola_xy_data_by_simplest_focus(xp, yp, x_min, x_max, y_min, y_max):
    return get_parabola_xy_data_by_standard_equation(
        *get_parabola_equation_coefficient_by_simplest_focus(xp, yp), x_min, x_max, y_min, y_max)


def get_parabola_equation_coefficient_by_focus_line(xp, yp, x1, y1, x2, y2):
    x1_x2 = x1 - x2
    y1_y2 = y1 - y2
    x1_x2_2 = x1_x2 ** 2
    y1_y2_2 = y1_y2 ** 2
    x1_x2_y1_y2 = x1_x2 * y1_y2
    dd = x1_x2_2 + y1_y2_2

    a11 = x1_x2_2 / dd
    a12 = x1_x2_y1_y2 / dd
    b1 = x1 - x1_x2_2 / dd * x1 - x1_x2_y1_y2 / dd * y1
    a22 = y1_y2_2 / dd
    b2 = y1 - x1_x2_y1_y2 / dd * x1 - y1_y2_2 / dd * y1

    a11 -= 1
    a22 -= 1

    return [a11 ** 2 + a12 ** 2 - 1,
            a11 * a12 + a12 * a22,
            a12 ** 2 + a22 ** 2 - 1,
            a11 * b1 + a12 * b2 + xp,
            a12 * b1 + a22 * b2 + yp,
            b1 ** 2 + b2 ** 2 - xp ** 2 - yp ** 2]


def get_parabola_xy_data_by_focus_point(xp, yp, xv, yv, x_min, x_max, y_min, y_max):
    p = get_distance_by_tow_point(xv, yv, xp, yp)
    t1, t2 = get_transform_vector_to_y_up(xp, yp, xv, yv)

    def f(x):
        return x ** 2 / (2 * p)

    center_x = (x_min + x_max) / 2
    center_y = (y_min + y_max) / 2
    x_lim = x_max - x_min
    center_x_new, center_y_new = t2(center_x, center_y)
    x_lim_new = 0.71 * x_lim

    x_set = linspace(center_x_new - x_lim_new, center_x_new + x_lim_new, 200)
    y_set = f(x_set)

    x_set_new, y_set_new = t1(x_set, y_set)

    return [x_set_new, y_set_new]
