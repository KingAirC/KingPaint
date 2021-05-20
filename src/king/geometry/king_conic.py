from .king_curve import KingCurve
from ..core.king_figure import KingFigure
from ..alg.conic_alg import *
from ..alg.plane_geometry_alg import get_edge_two_point_by_line
from ..alg.basic_alg import nan
from ..alg.circle_alg import get_circle_xy_data_by_center_radius
from ..alg.ellipse_alg import get_ellipse_xy_data_by_standard_equation
from ..alg.hyperbola_alg import get_hyperbola_xy_data_by_standard_equation
from ..alg.parabola_alg import get_parabola_xy_data_by_standard_equation


class KingConic(KingCurve):
    conic_type_cls_var = None

    def __init__(self, depends=(), essential_data=None, create_type=1, infinite=True):
        self.conic_type = None
        self.conic_basic_data = None
        super(KingConic, self).__init__(depends=depends, essential_data=essential_data, create_type=create_type,
                                        infinite=infinite)

    def generate_xy_data_from_basic_data(self):
        x_min, x_max = KingFigure().get_x_lim()
        y_min, y_max = KingFigure().get_y_lim()
        t1, t2, translation_coefficient = get_simplest_conic_equation_and_transform_by_conic_equation(*self.basic_data)
        type_basic_data = get_conic_type_and_basic_data_by_simplest_equation(*translation_coefficient)
        kind = type_basic_data[0]
        self.conic_type = kind
        if kind == CONIC_TYPE_CAN_NOT_PLOT:
            self.conic_basic_data = [[], []]
            return self.conic_basic_data
        if kind == CONIC_TYPE_POINT:
            self.conic_basic_data = t1(0, 0)
            return self.conic_basic_data
        if kind == CONIC_TYPE_LINE:
            x1, y1 = t1(*type_basic_data[1][0])
            x2, y2 = t1(*type_basic_data[1][1])
            basic_data = get_edge_two_point_by_line(x1, y1, x2, y2, x_min, x_max, y_min, y_max)
            self.conic_basic_data = basic_data
            return [[basic_data[0][0], basic_data[1][0]], [basic_data[0][1], basic_data[1][1]]]
        if kind == CONIC_TYPE_PARALLEL_LINE or kind == CONIC_TYPE_INTERSECT_LINE:
            x1, y1 = type_basic_data[1][0][0]
            x2, y2 = type_basic_data[1][0][1]
            x3, y3 = type_basic_data[1][1][0]
            x4, y4 = type_basic_data[1][1][1]
            x1, y1 = t1(x1, y1)
            x2, y2 = t1(x2, y2)
            x3, y3 = t1(x3, y3)
            x4, y4 = t1(x4, y4)
            l1 = get_edge_two_point_by_line(x1, y1, x2, y2, x_min, x_max, y_min, y_max)
            l2 = get_edge_two_point_by_line(x3, y3, x4, y4, x_min, x_max, y_min, y_max)
            self.conic_basic_data = [l1, l2]
            return [[l1[0][0], l1[1][0], nan, l2[0][0], l2[1][0]], [l1[0][1], l1[1][1], nan, l2[0][1], l2[1][1]]]
        if kind == CONIC_TYPE_CIRCLE:
            o = t1(0, 0)
            r = type_basic_data[1]
            self.conic_basic_data = [o, r]

            return get_circle_xy_data_by_center_radius(*o, r)
        if kind == CONIC_TYPE_ELLIPSE:
            standard_xy = \
                get_ellipse_xy_data_by_standard_equation(-translation_coefficient[0] / translation_coefficient[5],
                                                         0,
                                                         -translation_coefficient[2] / translation_coefficient[5],
                                                         0, 0, -1)
            self.conic_basic_data = [t1(*type_basic_data[1][0]), t1(*type_basic_data[1][1]), type_basic_data[1][2]]

            return t1(*standard_xy)
        if kind == CONIC_TYPE_HYPERBOLA:
            center = t2((x_min + x_max) / 2, (y_min + y_max) / 2)
            x_lim = 0.71 * (x_max - x_min)
            y_lim = 0.71 * (y_max - y_min)

            standard_xy = \
                get_hyperbola_xy_data_by_standard_equation(translation_coefficient[0] / translation_coefficient[5],
                                                           0,
                                                           translation_coefficient[2] / translation_coefficient[5],
                                                           0, 0, 1,
                                                           center[0] - x_lim,
                                                           center[0] + x_lim,
                                                           center[1] - y_lim,
                                                           center[1] + y_lim)
            self.conic_basic_data = [t1(*type_basic_data[1][0]), t1(*type_basic_data[1][1]), type_basic_data[1][2]]

            return t1(*standard_xy)
        if kind == CONIC_TYPE_PARABOLA:
            center = t2((x_min + x_max) / 2, (y_min + y_max) / 2)
            x_lim = 0.71 * (x_max - x_min)
            y_lim = 0.71 * (y_max - y_min)

            standard_xy = get_parabola_xy_data_by_standard_equation(*translation_coefficient,
                                                                    center[0] - x_lim,
                                                                    center[0] + x_lim,
                                                                    center[1] - y_lim,
                                                                    center[1] + y_lim)
            self.conic_basic_data = [t1(*type_basic_data[1][0]), t1(*type_basic_data[1][1])]

            return t1(*standard_xy)
