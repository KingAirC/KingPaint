from .alg.basic_alg import *
from .alg.circle_alg import *
from .alg.conic_alg import *
from .alg.ellipse_alg import *
from .alg.hyperbola_alg import *
from .alg.parabola_alg import *
from .alg.plane_geometry_alg import *
from .alg.triangle_center_alg import *
from .core.king_animation import *
from .core.king_decorater import *
from .core.king_decorater_multi_geometry import *
from .core.king_figure import *
from .core.king_geometry import *
from .geometry.king_conic import *
from .geometry.king_conic_generator import *
from .geometry.king_conic_graph import *
from .geometry.king_conic_graph_generator import *
from .geometry.king_curve import *
from .geometry.king_empty_geometry import *
from .geometry.king_equation import *
from .geometry.king_function import *
from .geometry.king_parametric_equation import *
from .geometry.king_plane_geometry_graph import *
from .geometry.king_plane_geometry_graph_generator import *
from .geometry.king_regular_polygon import *
from .geometry.king_triangle_center_generator import outer as ot
from .geometry.king_triangle_center_generator import median as md
from .geometry.king_triangle_center_generator import incenter as it
from .geometry.king_triangle_center_generator import orthocenter as oc
from .geometry_attribute.affine import *
from .geometry_attribute.angle import *
from .geometry_attribute.distance import *

__all__ = ['alg', 'core', 'geometry', 'geometry_attribute']
conic_class_list = [KingConic, KingCircle, KingEllipse, KingHyperbola, KingParabola]
figure = KingFigure()
p_nan = KingPoint(essential_data=[nan, nan])


def point(x=None, y=None, p_list=None, label=None, color=None, from_number=1):
    if x is not None and y is not None:
        p = KingPoint(essential_data=[x, y])
        if label is not None:
            p.text.set_text(label)
        if color is not None:
            p.set_markerfacecolor(color)
            p.set_markeredgecolor(color)
        return p
    if p_list is not None:
        ps = []
        for i in p_list:
            ps.append(KingPoint(essential_data=i))
        if label is not None and from_number is not None:
            for i in range(len(ps)):
                ps[i].text.set_text(label + str(from_number + i))
        if color is not None:
            for p in ps:
                p.set_markerfacecolor(color)
                p.set_markeredgecolor(color)
        return ps


def line(p1=None, p2=None, k=None, b=None, A=None, B=None, C=None):
    if isinstance(p1, KingPoint) and isinstance(p2, KingPoint):
        return KingLine(depends=[p1, p2])
    if k is not None and b is not None:
        return line_kb(essential_data=[k, b])
    if A is not None and B is not None and C is not None:
        return line_general(essential_data=[A, B, C])
    if k is not None and isinstance(p1, KingPoint):
        return line_point_k(depends=[p1], essential_data=[k])
    if k is not None and isinstance(p2, KingPoint):
        return line_point_k(depends=[p2], essential_data=[k])


def line_segment(p1, p2):
    return KingLineSegment(depends=[p1, p2])


def middle(o1, o2):
    if isinstance(o1, KingPoint) and isinstance(o2, KingPoint):
        return point_middle(depends=[o1, o2])


def rotate(o1, o2, t):
    if isinstance(o1, KingPoint) and isinstance(o2, KingPoint):
        return point_rotate(depends=[o1, o2], essential_data=[t])


def vertical(p, l):
    if isinstance(p, KingPoint) and isinstance(l, KingLine):
        return point_vertical_point_line(depends=[p, l])
    if isinstance(p, KingLine) and isinstance(l, KingPoint):
        return point_vertical_point_line(depends=[l, p])


def symmetry_center(o):
    if isinstance(o, KingConic):
        return point_conic_symmetry_center(depends=[o])


def symmetric(p, l):
    if isinstance(p, KingPoint):
        if isinstance(l, KingLine):
            return point_symmetric_point_line(depends=[p, l])
        if isinstance(l, KingPoint):
            return point_symmetric_point(depends=[p, l])
    if isinstance(p, KingLine) and isinstance(l, KingPoint):
        return point_symmetric_point_line(depends=[l, p])


def intersect(o1, o2):
    if isinstance(o1, KingLine):
        if isinstance(o2, KingLine):
            return point_intersect_by_two_line(depends=[o1, o2])
        if is_object_in_class_list(o2, conic_class_list):
            return point_intersect_line_conic(depends=[o1, o2])
    if isinstance(o2, KingLine):
        if is_object_in_class_list(o1, conic_class_list):
            return point_intersect_line_conic(depends=[o2, o1])


def asymptote(o):
    if isinstance(o, KingConic) or isinstance(o, KingHyperbola):
        return conic_asymptote(depends=[o])


def symmetry_lines(o):
    if isinstance(o, KingConic):
        return conic_symmetry_lines(depends=[o])


def tangent_line(p, o):
    if isinstance(o, KingConic) or is_object_in_class_list(o, conic_class_list):
        return tangent_line_by_conic(depends=[p, o])


def conic(coefficient=(), p_list=()):
    if len(coefficient) == 6:
        return KingConic(essential_data=coefficient)
    if len(p_list) == 5:
        return five_point_conic(depends=p_list)


def circle(o=None, r=None, p=None, p1=None, p2=None, p3=None):
    if isinstance(o, KingPoint):
        if r is not None:
            return KingCircle(depends=[o], essential_data=[r])
        if isinstance(p, KingPoint):
            return circle_center_edge_point(depends=[o, p])
    if isinstance(p1, KingPoint) and isinstance(p2, KingPoint) and isinstance(p3, KingPoint):
        return circle_three_point(depends=[p1, p2, p3])


def ellipse(e1=None, e2=None, p=None, add=None, v1=None, v2=None, b=None):
    if isinstance(e1, KingPoint) and isinstance(e2, KingPoint):
        if isinstance(p, KingPoint):
            return ellipse_three_point(depends=[e1, e2, p])
        if add is not None:
            return KingEllipse(depends=[e1, e2], essential_data=[add])
    if isinstance(v1, KingPoint) and isinstance(v2, KingPoint) and b is not None:
        return ellipse_isosceles_triangle(depends=[v1, v2], essential_data=[b])


def hyperbola(e1=None, e2=None, p=None, diff=None):
    if isinstance(e1, KingPoint) and isinstance(e2, KingPoint):
        if isinstance(p, KingPoint):
            return hyperbola_three_point(depends=[e1, e2, p])
        if diff is not None:
            return KingHyperbola(depends=[e1, e2], essential_data=[diff])


def parabola(o1, o2):
    if isinstance(o1, KingPoint):
        if isinstance(o2, KingPoint):
            return KingParabola(depends=[o1, o2])
        if isinstance(o2, KingLine):
            return parabola_point_line(depends=[o1, o2])
    if isinstance(o1, KingLine):
        if isinstance(o2, KingPoint):
            return parabola_point_line(depends=[o2, o1])


def orthocenter(p1, p2, p3):
    if isinstance(p1, KingPoint) and isinstance(p2, KingPoint) and isinstance(p3, KingPoint):
        return oc(depends=[p1, p2, p3])


def median(p1, p2, p3):
    if isinstance(p1, KingPoint) and isinstance(p2, KingPoint) and isinstance(p3, KingPoint):
        return md(depends=[p1, p2, p3])


def incenter(p1, p2, p3):
    if isinstance(p1, KingPoint) and isinstance(p2, KingPoint) and isinstance(p3, KingPoint):
        return it(depends=[p1, p2, p3])


def outer(p1, p2, p3):
    if isinstance(p1, KingPoint) and isinstance(p2, KingPoint) and isinstance(p3, KingPoint):
        return ot(depends=[p1, p2, p3])


def regular_polygon(o, p, n):
    if isinstance(o, KingPoint) and isinstance(p, KingPoint):
        return KingRegularPolygon(depends=[o, p], essential_data=[n])


def function(f, x_min=None, x_max=None, count=None):
    return KingFunction(essential_data={'function': f, 'x_min': x_min, 'x_max': x_max, 'count': count})


def equation(z):
    return KingEquation(essential_data=[z])


def parametric_equation(x, y, t_min, t_max, count=None):
    return KingParametricEquation(essential_data={'x': x, 'y': y, 't_min': t_min, 't_max': t_max, 'count': count})
