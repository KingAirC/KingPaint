from ..core.king_decorater import geometry_generate
from .king_conic import KingConic
from ..alg.conic_alg import get_conic_mat_by_five_point, get_conic_coefficient
from ..alg.basic_alg import rref


def _five_point_conic(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5):
    mat = get_conic_mat_by_five_point(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5)
    mat = rref(mat)
    coefficient = get_conic_coefficient(mat)

    return coefficient


@geometry_generate(cls=KingConic)
def five_point_conic(depends=(), essential_data=None):
    x1, y1 = depends[0].basic_data
    x2, y2 = depends[1].basic_data
    x3, y3 = depends[2].basic_data
    x4, y4 = depends[3].basic_data
    x5, y5 = depends[4].basic_data

    return _five_point_conic(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5)
