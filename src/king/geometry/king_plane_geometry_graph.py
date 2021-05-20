from ..core.king_figure import KingFigure
from .king_curve import KingCurve
from ..alg.plane_geometry_alg import get_edge_two_point_by_line


class KingPoint(KingCurve):
    def __init__(self, depends=(), essential_data=None, create_type=1):
        super(KingPoint, self).__init__(depends=depends, essential_data=essential_data, create_type=create_type)
        self.mouse_select_priority = 0
        self.set_marker('o')
        self.set_markersize(5)
        self.set_markerfacecolor('blue')
        self.set_markeredgecolor('black')

    def calc_essential_data_by_delta(self, delta):
        return [self.basic_data[0] + delta[0], self.basic_data[1] + delta[1]]

    def generate_xy_data_from_basic_data(self):
        return self.basic_data


class KingLine(KingCurve):
    def __init__(self, depends=(), essential_data=None, create_type=1):
        super(KingLine, self).__init__(depends=depends, essential_data=essential_data, create_type=create_type,
                                       infinite=True)

    def generate_basic_data(self, depends=(), essential_data=None):
        x1 = depends[0].basic_data[0]
        y1 = depends[0].basic_data[1]
        x2 = depends[1].basic_data[0]
        y2 = depends[1].basic_data[1]

        return get_edge_two_point_by_line(x1, y1, x2, y2, *KingFigure().get_x_lim(), *KingFigure().get_y_lim())

    def generate_xy_data_from_basic_data(self):
        return [[self.basic_data[0][0], self.basic_data[1][0]], [self.basic_data[0][1], self.basic_data[1][1]]]


class KingLineSegment(KingCurve):
    def __init__(self, depends=(), essential_data=None, create_type=1):
        super(KingLineSegment, self).__init__(depends=depends, essential_data=essential_data, create_type=create_type)

    def generate_basic_data(self, depends=(), essential_data=None):
        return [self.depends[0].basic_data, self.depends[1].basic_data]

    def generate_xy_data_from_basic_data(self):
        return [[self.basic_data[0][0], self.basic_data[1][0]],
                [self.basic_data[0][1], self.basic_data[1][1]]]
