from ..alg.circle_alg import get_circle_xy_data_by_center_radius
from ..alg.ellipse_alg import get_ellipse_xy_data_by_focus_add
from ..alg.hyperbola_alg import get_hyperbola_xy_data_by_focus_diff
from ..core.king_figure import KingFigure
from .king_curve import KingCurve
from ..alg.parabola_alg import get_parabola_xy_data_by_focus_point
from ..alg.conic_alg import CONIC_TYPE_CIRCLE, CONIC_TYPE_ELLIPSE, CONIC_TYPE_HYPERBOLA, CONIC_TYPE_PARABOLA


class KingCircle(KingCurve):
    conic_type_cls_var = CONIC_TYPE_CIRCLE

    def __init__(self, depends=(), essential_data=None, create_type=1):
        super(KingCircle, self).__init__(depends=depends, essential_data=essential_data,
                                         create_type=create_type)

    def generate_basic_data(self, depends=(), essential_data=None):
        return [self.depends[0].basic_data, self.essential_data[0]]

    def generate_xy_data_from_basic_data(self):
        x1, y1 = self.basic_data[0]
        r = self.basic_data[1]
        return get_circle_xy_data_by_center_radius(x1, y1, r)


class KingEllipse(KingCurve):
    conic_type_cls_var = CONIC_TYPE_ELLIPSE

    def __init__(self, depends=(), essential_data=None, create_type=1):
        super(KingEllipse, self).__init__(depends=depends, essential_data=essential_data,
                                          create_type=create_type)

    def generate_basic_data(self, depends=(), essential_data=None):
        return [self.depends[0].basic_data, self.depends[1].basic_data, self.essential_data[0]]

    def generate_xy_data_from_basic_data(self):
        x1, y1 = self.basic_data[0]
        x2, y2 = self.basic_data[1]
        b2 = self.basic_data[2]
        return get_ellipse_xy_data_by_focus_add(x1, y1, x2, y2, b2)


class KingHyperbola(KingCurve):
    conic_type_cls_var = CONIC_TYPE_HYPERBOLA

    def __init__(self, depends=(), essential_data=None, create_type=1):
        super(KingHyperbola, self).__init__(depends=depends, essential_data=essential_data, create_type=create_type,
                                            infinite=True)

    def generate_basic_data(self, depends=(), essential_data=None):
        return [depends[0].basic_data, depends[1].basic_data, essential_data[0]]

    def generate_xy_data_from_basic_data(self):
        x1 = self.basic_data[0][0]
        y1 = self.basic_data[0][1]
        x2 = self.basic_data[1][0]
        y2 = self.basic_data[1][1]
        b2 = self.basic_data[2]
        x_min, x_max = KingFigure().get_x_lim()
        y_min, y_max = KingFigure().get_y_lim()

        return get_hyperbola_xy_data_by_focus_diff(x1, y1, x2, y2, b2, x_min, x_max, y_min, y_max)


class KingParabola(KingCurve):
    conic_type_cls_var = CONIC_TYPE_PARABOLA

    def __init__(self, depends=(), essential_data=None, create_type=1):
        super(KingParabola, self).__init__(depends=depends, essential_data=essential_data, create_type=create_type,
                                           infinite=True)

    def generate_basic_data(self, depends=(), essential_data=None):
        return [depends[0].basic_data, depends[1].basic_data]

    def generate_xy_data_from_basic_data(self):
        xp, yp = self.basic_data[0]
        xv, yv = self.basic_data[1]
        x_min, x_max = KingFigure().get_x_lim()
        y_min, y_max = KingFigure().get_y_lim()

        return get_parabola_xy_data_by_focus_point(xp, yp, xv, yv, x_min, x_max, y_min, y_max)
