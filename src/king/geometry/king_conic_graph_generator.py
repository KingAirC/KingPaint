from .king_conic_graph import *
from ..alg.ellipse_alg import get_ellipse_basic_data_by_three_point, get_ellipse_basic_data_by_isosceles_triangle
from ..alg.plane_geometry_alg import get_distance_by_tow_point
from ..core.king_decorater import geometry_generate
from ..alg.plane_geometry_alg import get_vertical_point_by_point_line
from ..alg.basic_alg import *


@geometry_generate(cls=KingCircle)
def circle_center_edge_point(depends=(), essential_data=None):
    o_x = depends[0].basic_data[0]
    o_y = depends[0].basic_data[1]
    c_x = depends[1].basic_data[0]
    c_y = depends[1].basic_data[1]
    return [[o_x, o_y], get_distance_by_tow_point(o_x, o_y, c_x, c_y)]


@geometry_generate(cls=KingCircle)
def circle_three_point(depends=(), essential_data=None):
    mat = [[2 * p.basic_data[0], 2 * p.basic_data[1], 1, -(p.basic_data[0] ** 2 + p.basic_data[1] ** 2)]
           for p in depends]
    mat2 = rref(mat)
    if mat2[2][2] == 1:
        D = mat2[0][3]
        E = mat2[1][3]
        F = mat2[2][3]
        return [[-D, -E], sqrt(D ** 2 + E ** 2 - F)]
    return [[nan, nan], nan]


@geometry_generate(cls=KingEllipse)
def ellipse_three_point(depends=(), essential_data=None):
    x1, y1 = depends[0].basic_data
    x2, y2 = depends[1].basic_data
    x3, y3 = depends[2].basic_data

    return get_ellipse_basic_data_by_three_point(x1, y1, x2, y2, x3, y3)


@geometry_generate(cls=KingEllipse)
def ellipse_isosceles_triangle(depends=(), essential_data=None):
    p1x, p1y = depends[0].basic_data
    p2x, p2y = depends[1].basic_data
    b = essential_data[0]

    return get_ellipse_basic_data_by_isosceles_triangle(p1x, p1y, p2x, p2y, b)


@geometry_generate(cls=KingHyperbola)
def hyperbola_three_point(depends=(), essential_data=None):
    x1, y1 = depends[0].basic_data
    x2, y2 = depends[1].basic_data
    x3, y3 = depends[2].basic_data
    b2 = get_distance_by_tow_point(x1, y1, x3, y3) - get_distance_by_tow_point(x2, y2, x3, y3)

    return [depends[0].basic_data, depends[1].basic_data, b2]


@geometry_generate(cls=KingParabola)
def parabola_point_line(depends=(), essential_data=None):
    xp, yp = depends[0].basic_data
    x1, y1 = depends[1].basic_data[0]
    x2, y2 = depends[1].basic_data[1]
    xv, yv = get_vertical_point_by_point_line(xp, yp, x1, y1, x2, y2)
    return [[xp, yp], [xv, yv]]
