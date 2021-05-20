from ..core.king_figure import KingFigure
from .king_curve import KingCurve
from ..alg.basic_alg import linspace


class KingFunction(KingCurve):
    def __init__(self, depends=(), essential_data=None, create_type=1):
        """
        {'function': f, 'x_min': min, 'x_max': max, 'count': c}
        """
        super(KingFunction, self).__init__(depends=depends, essential_data=essential_data, create_type=create_type,
                                           infinite=True)

    def generate_basic_data(self, depends=(), essential_data=None):
        return essential_data

    def generate_xy_data_from_basic_data(self):
        x_min = self.basic_data['x_min']
        x_max = self.basic_data['x_max']
        count = self.basic_data['count']
        x_min_figure, x_max_figure = KingFigure().get_x_lim()
        if x_min is None:
            x_min = x_min_figure
        if x_max is None:
            x_max = x_max_figure
        if count is None:
            count = 100
        x = linspace(x_min, x_max, count)
        return [x, self.basic_data['function'](x)]
