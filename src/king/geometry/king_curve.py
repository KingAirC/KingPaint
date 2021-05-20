from ..core.king_geometry import KingGeometry
from matplotlib.pyplot import Line2D
import abc
from matplotlib.transforms import Affine2D
from matplotlib.text import Text


class KingCurve(KingGeometry, Line2D, metaclass=abc.ABCMeta):
    def __init__(self, depends=(), essential_data=None, create_type=1, infinite=False):
        self.text = Text(0, 0, '')
        super(KingGeometry, self).__init__([], [])
        super(KingCurve, self).__init__(depends=depends, essential_data=essential_data,
                                        create_type=create_type, infinite=infinite)
        self.text.set_text(self.get_label())
        self.mouse_select_priority = 2
        if create_type == 1:
            self.mouse_translation = True

    def set_visible(self, b):
        super(KingCurve, self).set_visible(b)
        if not b:
            self.mouse_translation = False

    def set_figure(self, figure):
        self.text.set_figure(figure)
        super(KingCurve, self).set_figure(figure)

    def set_axes(self, axes):
        self.text.set_axes(axes)
        super().set_axes(axes)

    def set_transform(self, transform):
        self.text.set_transform(transform + Affine2D().translate(2, 2))
        super().set_transform(transform)

    def set_data(self, x, y):
        if isinstance(x, list) and len(x) > 0:
            len_x = len(x)
            if len_x == 2:
                pos = ((x[0] + x[1]) / 2, (y[0] + y[1]) / 2)
            else:
                pos = (x[-1], y[-1])
            self.text.set_position(pos)
        else:
            self.text.set_position((x, y))
        super().set_data(x, y)

    def draw(self, renderer):
        super().draw(renderer)
        self.text.draw(renderer)

    @abc.abstractmethod
    def generate_xy_data_from_basic_data(self):
        pass

    def assign_basic_data_to_artist(self):
        self.set_data(*self.generate_xy_data_from_basic_data())
