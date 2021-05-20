from ..core.king_decorater import geometry_generate
from .king_plane_geometry_graph import KingPoint
from ..alg.triangle_center_alg import *


@geometry_generate(cls=KingPoint)
def orthocenter(depends=(), essential_data=None):
    p1 = depends[0]
    p2 = depends[1]
    p3 = depends[2]

    return get_orthocenter_by_three_point(*p1.basic_data, *p2.basic_data, *p3.basic_data)


@geometry_generate(cls=KingPoint)
def median(depends=(), essential_data=None):
    p1 = depends[0]
    p2 = depends[1]
    p3 = depends[2]

    return get_meidan_by_three_point(*p1.basic_data, *p2.basic_data, *p3.basic_data)


@geometry_generate(cls=KingPoint)
def incenter(depends=(), essential_data=None):
    p1 = depends[0]
    p2 = depends[1]
    p3 = depends[2]

    return get_incenter_by_three_point(*p1.basic_data, *p2.basic_data, *p3.basic_data)


@geometry_generate(cls=KingPoint)
def outer(depends=(), essential_data=None):
    p1 = depends[0]
    p2 = depends[1]
    p3 = depends[2]

    return get_outer_by_three_point(*p1.basic_data, *p2.basic_data, *p3.basic_data)
