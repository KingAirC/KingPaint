from ..core.king_geometry import KingGeometry
from matplotlib.pyplot import Artist
import numpy as np
from ..core.king_figure import KingFigure


class KingEquation(KingGeometry, Artist):
    def __init__(self, depends=(), essential_data=None, create_type=1):
        self.contour = None
        super(KingGeometry, self).__init__()
        super(KingEquation, self).__init__(depends=depends, essential_data=essential_data, create_type=create_type,
                                           infinite=True)
        self.mouse_select_priority = 1

    def assign_basic_data_to_artist(self):
        x = np.linspace(*KingFigure().get_x_lim(), 100)
        y = np.linspace(*KingFigure().get_y_lim(), 100)
        z = self.basic_data[0](*np.meshgrid(x, y))
        if self.contour is not None:
            for c in self.contour.collections:
                c.remove()
            del self.contour
        self.contour = KingFigure().ax.contour(x, y, z, 0)

    def contains(self, mouseevent):
        return False, {}
