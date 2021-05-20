from matplotlib.animation import FuncAnimation
from .king_figure import KingFigure
from ..alg.basic_alg import linspace


class KingAnimation:
    """
    Animation.
    Parameter:
    ----------
    artists : must be KingGeometry and Artist's instance list.
    essential_data_generators : A list of function which generates essential_data for each artists,
                                accept a parameter represent for frame.
    frames : Iterable or callable.
    interval : Time interval.
    See FuncAnimation.
    """
    def __init__(self, artists, essential_data_generators, frames=linspace(0, 10, 101), interval=50):
        self.artists = artists
        self.essential_data_generators = essential_data_generators
        self.frames = frames
        self.interval = interval
        self.count = len(artists)

        for a in artists:
            a.mouse_translation = False
        self.ani = FuncAnimation(KingFigure().fig, self.update, frames=frames, interval=interval, blit=True)

    def update(self, frame):
        result = []

        for i in range(self.count):
            result.extend(self.artists[i].update_affected(new_essential_data=self.essential_data_generators[i](frame)))

        return result
