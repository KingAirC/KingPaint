from .basic_alg import sqrt, unit_circle
from .plane_geometry_alg import get_transform_vector_to_y_up, get_distance_by_tow_point


def get_ellipse_focus_add_by_standard_equation(a11, a12, a22, a1, a2, a0):
    """
    a11 = 1/a^2
    a22 = 1/b^2
    a12 = a1 = a2 = 0
    a0 = -1
    """
    if a11 < a22:
        a11_1 = 1 / a11
        c = sqrt(a11_1 - 1 / a22)
        return [[c, 0], [-c, 0], 2 * sqrt(a11_1)]
    a22_1 = 1 / a22
    c = sqrt(a22_1 - 1 / a11)
    return [[0, c], [0, -c], 2 * sqrt(a22_1)]


def get_ellipse_equation_coefficient_by_simplest_focus_add(x1, y1, x2, y2, add):
    """
    [1/a^2, 0, 1/b^2, 0, 0, -1]
    """
    if y1 == 0:
        a = add / 2
        aa = a * a
        c = abs(x1)
        bb = aa - c ** 2
        return [1 / aa, 0, 1 / bb, 0, 0, -1]
    b = add / 2
    bb = b * b
    c = abs(y1)
    aa = bb - c ** 2
    return [1 / aa, 0, 1 / bb, 0, 0, -1]


def get_ellipse_xy_data_by_standard_equation(a11, a12, a22, a1, a2, a0):
    a = 1 / sqrt(a11)
    b = 1 / sqrt(a22)
    return [unit_circle[0] * a, unit_circle[1] * b]


def get_ellipse_xy_data_by_simplest_focus_add(x1, y1, x2, y2, add):
    return get_ellipse_xy_data_by_standard_equation(
        *get_ellipse_equation_coefficient_by_simplest_focus_add(x1, y1, x2, y2, add))


def get_ellipse_xy_data_by_focus_add(x1, y1, x2, y2, add):
    b = add / 2
    dd = (x1 - x2) ** 2 + (y1 - y2) ** 2
    cc = dd / 4
    bb = b ** 2
    aa = bb - cc
    a = sqrt(aa)
    x_data = unit_circle[0] * a
    y_data = unit_circle[1] * b
    t1, t2 = get_transform_vector_to_y_up(x1, y1, x2, y2)
    return t1(x_data, y_data)


def get_ellipse_basic_data_by_three_point(x1, y1, x2, y2, x3, y3):
    return [[x1, y1], [x2, y2],
            get_distance_by_tow_point(x1, y1, x3, y3) + get_distance_by_tow_point(x2, y2, x3, y3)]


def get_ellipse_basic_data_by_isosceles_triangle(p1x, p1y, p2x, p2y, b):
    ox, oy = (p1x + p2x) / 2, (p1y + p2y) / 2
    l1 = get_distance_by_tow_point(p1x, p1y, p2x, p2y)
    a = l1 / 2
    if b < a:
        cc = a ** 2 - b ** 2
        c = sqrt(cc)
        c_a = c / a
        cx1 = ox + c_a * (p1x - ox)
        cy1 = oy + c_a * (p1y - oy)
        cx2 = 2 * ox - cx1
        cy2 = 2 * oy - cy1
        return [[cx1, cy1], [cx2, cy2], l1]
    else:
        cc = b ** 2 - a ** 2
        c = sqrt(cc)
        add = 2 * b
        if p1y == p2y:
            return [[ox, p1y + c], [ox, p1y - c], add]
        k = (p2x - p1x) / (p1y - p2y)
        x = c / sqrt(1 + k ** 2)
        cx1 = x + ox
        cy1 = k * x + oy
        cx2 = 2 * ox - cx1
        cy2 = 2 * oy - cy1
        return [[cx1, cy1], [cx2, cy2], add]
