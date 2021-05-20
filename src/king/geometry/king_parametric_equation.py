from .king_curve import KingCurve
from ..alg.basic_alg import linspace


class KingParametricEquation(KingCurve):
    def __init__(self, depends=(), essential_data=None, create_type=1):
        """
        {'x': x, 'y': y, 't_min': min, 't_max': max, 'count': c}
        """
        super(KingParametricEquation, self).__init__(depends=depends, essential_data=essential_data,
                                                     create_type=create_type)

    def generate_basic_data(self, depends=(), essential_data=None):
        return essential_data

    def generate_xy_data_from_basic_data(self):
        t_min = self.basic_data['t_min']
        t_max = self.basic_data['t_max']
        count = self.basic_data['count']
        x = self.basic_data['x']
        y = self.basic_data['y']
        if count is None:
            count = 100

        t = linspace(t_min, t_max, count)
        return [x(t), y(t)]
