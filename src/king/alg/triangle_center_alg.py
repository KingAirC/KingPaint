from .basic_alg import rref
from .plane_geometry_alg import get_distance_by_tow_point


def get_orthocenter_by_three_point(x1, y1, x2, y2, x3, y3):
    a11 = x2 - x1
    a12 = y2 - y1
    a21 = x2 - x3
    a22 = y2 - y3
    b1 = a11 * x3 + a12 * y3
    b2 = a21 * x1 + a22 * y1

    mat = [
        [a11, a12, b1],
        [a21, a22, b2]
    ]

    rref_mat = rref(mat)

    return [rref_mat[0][2], rref_mat[1][2]]


def get_meidan_by_three_point(x1, y1, x2, y2, x3, y3):
    x4 = (x1 + x2) / 2
    y4 = (y1 + y2) / 2
    return [x3 / 3 + 2 * x4 / 3, y3 / 3 + 2 * y4 / 3]


def get_incenter_by_three_point(x1, y1, x2, y2, x3, y3):
    a = get_distance_by_tow_point(x2, y2, x3, y3)
    b = get_distance_by_tow_point(x1, y1, x3, y3)
    c = get_distance_by_tow_point(x1, y1, x2, y2)
    abc = a + b + c

    return [(a * x1 + b * x2 + c * x3) / abc, (a * y1 + b * y2 + c * y3) / abc]


def get_outer_by_three_point(x1, y1, x2, y2, x3, y3):
    x4 = (x1 + x2) / 2
    y4 = (y1 + y2) / 2
    x5 = (x1 + x3) / 2
    y5 = (y1 + y3) / 2
    a11 = x1 - x2
    a12 = y1 - y2
    a21 = x1 - x3
    a22 = y1 - y3
    b1 = a11 * x4 + a12 * y4
    b2 = a21 * x5 + a22 * y5
    mat = [
        [a11, a12, b1],
        [a21, a22, b2]
    ]
    rref_mat = rref(mat)

    return [rref_mat[0][2], rref_mat[1][2]]
