from ..core.king_geometry import KingGeometry
from matplotlib.pyplot import Artist


class EmptyGeometry(KingGeometry, Artist):
    def __init__(self, depends=(), essential_data=None, create_type=2):
        super(KingGeometry, self).__init__()
        super(EmptyGeometry, self).__init__(depends=depends, essential_data=essential_data, create_type=create_type,
                                            infinite=True)
        self.set_visible(False)
        self.set_animated(False)
        self.set_picker(False)

    def contains(self, mouseevent):
        return False, {}
