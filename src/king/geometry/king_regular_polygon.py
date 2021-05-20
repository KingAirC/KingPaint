from ..core.king_geometry import KingGeometry
from matplotlib.pyplot import Artist
from ..alg.basic_alg import pi_2
from ..geometry.king_plane_geometry_graph_generator import point_rotate
from ..geometry.king_plane_geometry_graph import KingLineSegment


class KingRegularPolygon(KingGeometry, Artist):
    def __init__(self, depends=(), essential_data=None, create_type=1):
        super(KingGeometry, self).__init__()
        super(KingRegularPolygon, self).__init__(depends=depends, essential_data=essential_data,
                                                 create_type=create_type)
        self.mouse_select_priority = 1
        if create_type == 1:
            self.mouse_translation = True
        t = pi_2 / essential_data[0]
        i = 0
        v = [depends[1]]
        e = []
        self.vertex = v
        self.edge = e
        n = essential_data[0] - 1
        while i < n:
            v.append(point_rotate(depends=[depends[0], v[i]], essential_data=[t]))
            e.append(KingLineSegment(depends=[v[i], v[i + 1]]))
            i += 1
        e.append(KingLineSegment(depends=[v[0], v[i]]))

    def contains(self, mouseevent):
        return False, {}
