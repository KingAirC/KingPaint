import abc
from .king_figure import KingFigure
from matplotlib.pyplot import Artist


class KingGeometry(metaclass=abc.ABCMeta):
    def __init__(self, depends=(), essential_data=None, create_type=1, infinite=False):
        if isinstance(self, Artist):
            self.set_animated(True)
            self.set_picker(True)
            KingFigure().add_artist(self)

        # Call backs when invoke update_self.
        self.call_backs = []

        # Update search flag.
        self.searched = False

        # Depends KingGeometry object list.
        self.depends = depends

        # Essential data supplement for depends.
        self._essential_data = essential_data

        # Basic data for assign Artist's init method.
        self._basic_data = None

        # KingGeometry who depends on this.
        self.feeds = []

        # A KingGeometry object can be instanced by tow methods.
        # 1: Free (can by moved by mouse)
        # 2: NoFree (can not move directly by mouse)
        self.create_type = create_type

        # Allow mouse translation. default False
        self.mouse_translation = False

        # Mouse select priority. The smallest first.
        self.mouse_select_priority = 10

        if create_type == 1:
            self.init()
        if infinite:
            KingFigure().inf_geometry.append(self)

    def append_call_back(self, f):
        self.call_backs.append(f)
        f(self)

    @property
    def basic_data(self):
        return self._basic_data

    @basic_data.setter
    def basic_data(self, basic_data):
        self._basic_data = basic_data

    @property
    def essential_data(self):
        return self._essential_data

    def set_depends_feeds(self):
        for node in self.depends:
            node.__add_feeds(self)

    def __add_feeds(self, node):
        self.feeds.append(node)

    def init(self):
        self.set_depends_feeds()
        self._basic_data = self.generate_basic_data(self.depends, self._essential_data)
        self.assign_basic_data_to_artist()
        if not KingFigure().init_delay_update:
            KingFigure().update()

    def generate_basic_data(self, depends=(), essential_data=None):
        """
            Default method to generate basic data.
        you can not use the parameter. you can only use self attribute.
        you might override this.
        :return:
        """
        return self._essential_data

    def assign_basic_data_to_artist(self):
        """
            Assign basic data to Artist's derived classes.
        :return:
        """
        pass

    def update_self(self, new_essential_data=None):
        """
            Update self.
        :return:
        """
        if new_essential_data is not None:
            self._essential_data = new_essential_data
        self._basic_data = self.generate_basic_data(self.depends, self._essential_data)
        self.assign_basic_data_to_artist()
        for func in self.call_backs:
            func(self)

    def update_affected(self, new_essential_data=None, repaint=True):
        """
            Update affected.
        :return: All affected artists.
        """
        KingFigure().clear_searched()

        self.update_self(new_essential_data)
        self.searched = True
        result = [self]
        queue = []
        for f in self.feeds:
            if not f.searched:
                queue.append(f)
                result.append(f)
                f.searched = True

        while len(queue) > 0:
            head = queue.pop(0)
            for f in head.feeds:
                if not f.searched:
                    queue.append(f)
                    result.append(f)
                    f.searched = True
            head.update_self()
        if repaint:
            KingFigure().update()
        return result

    def calc_essential_data_by_delta(self, delta):
        """
            Calculate essential data by delta.
        :param delta:
        :return: essential data
        """
        return self._essential_data

    def translation(self, delta):
        """
            Translation method. It can translation by mouse if and only if the depends geometry has no depends.
            Parameters
            ----------
            delta : (float, float)
                    delta x and delta y.
        :return:
        """
        ready2update = []
        ready2update.extend(self.depends)
        ready2update.append(self)
        KingFigure().clear_searched()
        for a in ready2update:
            if a.calc_essential_data_by_delta is None:
                esd = None
            else:
                esd = a.calc_essential_data_by_delta(delta)
            a.update_self(esd)
            a.searched = True
        for b in ready2update:
            queue = []
            for f in b.feeds:
                if not f.searched:
                    queue.append(f)
                    f.searched = True
            while len(queue) > 0:
                head = queue.pop(0)
                for f in head.feeds:
                    if not f.searched:
                        queue.append(f)
                        f.searched = True
                head.update_self()
