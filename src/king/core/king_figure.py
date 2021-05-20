import matplotlib.pyplot as plt
from .king_decorater import singleton


@singleton
class KingFigure:
    def __init__(self):
        # plt.rcParams['toolbar'] = 'none'
        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.canvas = self.fig.canvas
        self.artists = self.ax.artists
        self.background = None
        self.scroll_rate = 0.1
        self.epsilon = 0.2

        self.old_x = None
        self.old_y = None
        self.selected_geometry_list = []
        self.is_selected_geometry = None

        # The geometry has a infinite bound. such as line, hyperbola, etc.
        # it should be repaint when the axis's limit changed.
        self.inf_geometry = []

        # Whether delay update when create a geometry.
        self.init_delay_update = False

        # self.canvas.manager.window.showMaximized()
        self.ax.spines['top'].set_color('none')
        self.ax.spines['right'].set_color('none')
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.spines['bottom'].set_position(('data', 0))
        self.ax.yaxis.set_ticks_position('left')
        self.ax.spines['left'].set_position(('data', 0))
        x_lim = y_lim = 20
        self.set_x_lim(-x_lim, x_lim)
        self.set_y_lim(-y_lim, y_lim)
        self.ax.set_aspect(1)

        self.ax.grid()

        self.canvas.mpl_connect("scroll_event", self.on_scroll)
        self.canvas.mpl_connect("draw_event", self.on_draw)
        self.canvas.mpl_connect('pick_event', self.on_pick)
        self.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.canvas.mpl_connect('button_release_event', self.on_button_release)
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

        self.ax.callbacks.connect('xlim_changed', self.on_lim_changed)

    def show(self):
        self.fig.show()

    def on_lim_changed(self, event):
        for a in self.inf_geometry:
            a.update_self()

    def set_x_lim(self, x_min, x_max):
        self.ax.set_xlim(left=x_min, right=x_max)

    def set_y_lim(self, y_min, y_max):
        self.ax.set_ylim(bottom=y_min, top=y_max)

    def get_x_lim(self):
        return self.ax.get_xlim()

    def get_y_lim(self):
        return self.ax.get_ylim()

    def on_scroll(self, event):
        if event.inaxes is None:
            return
        x_min, x_max = self.get_x_lim()
        y_min, y_max = self.get_y_lim()
        x_mouse, y_mouse = event.xdata, event.ydata
        rate = self.scroll_rate if event.button == 'up' else -self.scroll_rate
        delta_l = (x_mouse - x_min) * rate
        delta_r = (x_max - x_mouse) * rate
        delta_u = (y_max - y_mouse) * rate
        delta_d = (y_mouse - y_min) * rate
        x_min_new, x_max_new = x_min + delta_l, x_max - delta_r
        y_min_new, y_max_new = y_min + delta_d, y_max - delta_u
        self.epsilon *= (1 - rate)
        self.set_x_lim(x_min_new, x_max_new)
        self.set_y_lim(y_min_new, y_max_new)
        self.canvas.draw_idle()

    def add_artist(self, artist):
        self.ax.add_artist(artist)

    def do_draw(self):
        for a in self.artists:
            self.ax.draw_artist(a)

    def on_draw(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.do_draw()

    def update(self):
        if self.background is None:
            self.canvas.draw()
        else:
            self.canvas.restore_region(self.background)
            self.do_draw()
            self.canvas.blit(self.ax.bbox)
        self.canvas.flush_events()

    def on_pick(self, event):
        self.selected_geometry_list.append(event.artist)
        for a in self.selected_geometry_list:
            if self.is_selected_geometry is None:
                self.is_selected_geometry = a
                continue
            if a.mouse_select_priority < self.is_selected_geometry.mouse_select_priority:
                self.is_selected_geometry = a

    def on_button_press(self, event):
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        self.old_x = event.xdata
        self.old_y = event.ydata

    def on_mouse_move(self, event):
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        if self.is_selected_geometry is None:
            return
        if not self.is_selected_geometry.mouse_translation:
            return
        delta_x = event.xdata - self.old_x
        delta_y = event.ydata - self.old_y
        self.old_x = event.xdata
        self.old_y = event.ydata
        self.is_selected_geometry.translation((delta_x, delta_y))
        self.update()

    def on_button_release(self, event):
        self.selected_geometry_list = []
        self.is_selected_geometry = None

    def clear_searched(self):
        for a in self.artists:
            a.searched = False
