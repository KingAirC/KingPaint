from .king_plane_geometry_graph import *
from ..alg.plane_geometry_alg import get_middle_point_by_two_point, get_rotate_point_by_two_point, \
    get_vertical_point_by_point_line, get_symmetric_point_by_point_line, get_point_by_matrix, \
    get_intersect_point_corr_by_four_point, get_symmetric_point_by_point
from ..core.king_decorater import geometry_generate
from ..core.king_decorater_multi_geometry import geometries_generate
from ..core.king_figure import KingFigure
from math import inf
from ..alg.basic_alg import nan, pi_half, tow_empty_line_basic_data, empty_line_basic_data, empty_point_basic_data
from ..alg.conic_alg import intersect_line_conic, get_central_conic_equation_coefficient_by_focus_d, \
    get_coefficient_by_conic
from ..alg.conic_alg import get_conic_symmetry_center, get_conic_asymptote_vector, get_diameter_direction_by_conic, \
    conic_tangent_vector
from ..geometry.king_conic import KingConic
from ..geometry.king_conic_graph import KingHyperbola


@geometry_generate(cls=KingPoint)
def point_middle(depends=(), essential_data=None):
    return get_middle_point_by_two_point(*depends[0].basic_data, *depends[1].basic_data)


@geometry_generate(cls=KingPoint)
def point_rotate(depends=(), essential_data=None):
    return get_rotate_point_by_two_point(depends[0].basic_data[0], depends[0].basic_data[1],
                                         depends[1].basic_data[0], depends[1].basic_data[1],
                                         essential_data[0])


@geometry_generate(cls=KingPoint)
def point_vertical_point_line(depends=(), essential_data=None):
    return get_vertical_point_by_point_line(*depends[0].basic_data,
                                            *depends[1].basic_data[0],
                                            *depends[1].basic_data[1])


@geometry_generate(cls=KingPoint)
def point_symmetric_point_line(depends=(), essential_data=None):
    return get_symmetric_point_by_point_line(*depends[0].basic_data, *depends[1].basic_data[0],
                                             *depends[1].basic_data[1])


@geometry_generate(cls=KingPoint)
def point_symmetric_point(depends=(), essential_data=None):
    return get_symmetric_point_by_point(*depends[0].basic_data, *depends[1].basic_data)


@geometry_generate(cls=KingPoint)
def point_matrix(depends=(), essential_data=None):
    x1, y1 = depends[0].basic_data
    mat = essential_data[0]
    return get_point_by_matrix(mat, x1, y1)


@geometry_generate(cls=KingPoint)
def point_intersect_by_two_line(depends=(), essential_data=None):
    l1 = depends[0]
    l2 = depends[1]
    p1 = l1.basic_data[0]
    p2 = l1.basic_data[1]
    p3 = l2.basic_data[0]
    p4 = l2.basic_data[1]

    return get_intersect_point_corr_by_four_point(*p1, *p2, *p3, *p4)


@geometry_generate(cls=KingPoint)
def point_on_curve(depends=(), essential_data=None):
    # TODO: point_on_curve
    return [nan, nan]


@geometry_generate(cls=KingPoint)
def point_conic_symmetry_center(depends=(), essential_data=None):
    center = get_conic_symmetry_center(*depends[0].basic_data)
    if center is None:
        return [nan, nan]
    return center


@geometry_generate(cls=KingLine)
def line_kb(depends=(), essential_data=None):
    k = essential_data[0]
    b = essential_data[1]
    if k == inf or k == -inf:
        y_min, y_max = KingFigure().get_y_lim()
        return [[b, y_min], [b, y_max]]

    x_min, x_max = KingFigure().get_x_lim()

    return [[x_min, k * x_min + b], [x_max, k * x_max + b]]


@geometry_generate(cls=KingLine)
def line_point_k(depends=(), essential_data=None):
    k = essential_data[0]
    if k == inf:
        y_min, y_max = KingFigure().get_y_lim()
        return [[depends[0].basic_data[0], y_min], [depends[0].basic_data[0], y_max]]
    x_min, x_max = KingFigure().get_x_lim()
    x1, y1 = depends[0].basic_data
    y1_k_x1 = y1 - k * x1
    return [[x_min, k * x_min + y1_k_x1], [x_max, k * x_max + y1_k_x1]]


@geometry_generate(cls=KingLine)
def line_general(depends=(), essential_data=None):
    a = essential_data[0]
    b = essential_data[1]
    c = essential_data[2]
    if a == 0:
        if b == 0:
            if c != 0:
                raise Exception("a=0,b=0,c!=0")
            return [[0, 0], [0, 0]]
        x_min, x_max = KingFigure().get_x_lim()
        _c_b = -c / b
        return [[x_min, _c_b], [x_max, _c_b]]
    if b == 0:
        if c == 0:
            return [[0, 0], [0, 0]]
        y_min, y_max = KingFigure().get_y_lim()
        _a_c = -a / c
        return [[_a_c, y_min], [_a_c, y_max]]
    x_min, x_max = KingFigure().get_x_lim()
    _a_b = -a / b
    _c_b = -c / b
    return [[x_min, _a_b * x_min + _c_b], [x_max, _a_b * x_max + _c_b]]


@geometries_generate(classes=[KingPoint], numbers=[2])
def point_intersect_line_conic(depends=(), essential_data=None):
    line = depends[0]
    ps = intersect_line_conic(*line.basic_data[0], *line.basic_data[1], *get_coefficient_by_conic(depends[1]))
    if ps is None:
        return [[nan] * 2] * 2
    if len(ps) == 1:
        return [ps[0], [nan, nan]]
    return [[ps[0][0], ps[0][1]], [ps[1][0], ps[1][1]]]


@geometries_generate(classes=[KingLine], numbers=[2])
def conic_asymptote(depends=(), essential_data=None):
    conic = depends[0]
    if isinstance(conic, KingConic):
        a11, a12, a22, a1, a2, a0 = conic.basic_data
    elif isinstance(conic, KingHyperbola):
        x1, y1 = conic.basic_data[0]
        x2, y2 = conic.basic_data[1]
        d = conic.basic_data[2]
        a11, a12, a22, a1, a2, a0 = get_central_conic_equation_coefficient_by_focus_d(x1, y1, x2, y2, d)
    else:
        return tow_empty_line_basic_data
    vec = get_conic_asymptote_vector(a11, a12, a22, a1, a2, a0)
    center = get_conic_symmetry_center(a11, a12, a22, a1, a2, a0)
    if center is None:
        return tow_empty_line_basic_data
    if vec is None:
        return tow_empty_line_basic_data
    return [get_edge_two_point_by_line(center[0], center[1], center[0] + 1, center[1] + vec[0],
                                       *KingFigure().get_x_lim(), *KingFigure().get_y_lim()),
            get_edge_two_point_by_line(center[0], center[1], center[0] + 1, center[1] + vec[1],
                                       *KingFigure().get_x_lim(), *KingFigure().get_y_lim())]


@geometries_generate(classes=[KingLine], numbers=[2])
def conic_symmetry_lines(depends=(), essential_data=None):
    conic = depends[0]
    a11, a12, a22, a1, a2, a0 = conic.basic_data
    vec = get_diameter_direction_by_conic(a11, a12, a22, a1, a2, a0)
    center = get_conic_symmetry_center(a11, a12, a22, a1, a2, a0)
    if center is None:
        center = conic.conic_basic_data[0]
        n = 0 if vec[2][0] == 0 else 1
        return [get_edge_two_point_by_line(center[0], center[1], center[0] + vec[n][0], center[1] + vec[n][1],
                                           *KingFigure().get_x_lim(), *KingFigure().get_y_lim()),
                empty_line_basic_data]
    return [get_edge_two_point_by_line(center[0], center[1], center[0] + vec[0][0], center[1] + vec[0][1],
                                       *KingFigure().get_x_lim(), *KingFigure().get_y_lim()),
            get_edge_two_point_by_line(center[0], center[1], center[0] + vec[1][0], center[1] + vec[1][1],
                                       *KingFigure().get_x_lim(), *KingFigure().get_y_lim())]


@geometries_generate(classes=[KingLine, KingPoint], numbers=[2, 2])
def tangent_line_by_conic(depends=(), essential_data=None):
    p = depends[0].basic_data
    vs = conic_tangent_vector(*p, *get_coefficient_by_conic(depends[1]))
    if vs is None:
        return empty_line_basic_data, empty_line_basic_data, empty_point_basic_data, empty_point_basic_data
    if len(vs) == 1:
        l1 = get_edge_two_point_by_line(p[0], p[1], p[0] + vs[0][0], p[1] + vs[0][1], *KingFigure().get_x_lim(),
                                        *KingFigure().get_y_lim())
        l2 = empty_line_basic_data
        if len(vs[0]) == 2:
            p1 = empty_point_basic_data
            p2 = empty_point_basic_data
        else:
            p1 = [p[0] + vs[0][2] * vs[0][0], p[1] + vs[0][2] * vs[0][1]]
            p2 = empty_point_basic_data
        return [l1, l2, p1, p2]

    l1 = get_edge_two_point_by_line(p[0], p[1], p[0] + vs[0][0], p[1] + vs[0][1], *KingFigure().get_x_lim(),
                                    *KingFigure().get_y_lim())
    l2 = get_edge_two_point_by_line(p[0], p[1], p[0] + vs[1][0], p[1] + vs[1][1], *KingFigure().get_x_lim(),
                                    *KingFigure().get_y_lim())
    p1 = [p[0] + vs[0][2] * vs[0][0], p[1] + vs[0][2] * vs[0][1]]
    p2 = [p[0] + vs[1][2] * vs[1][0], p[1] + vs[1][2] * vs[1][1]]

    return [l1, l2, p1, p2]
