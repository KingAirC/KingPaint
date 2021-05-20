from matplotlib.widgets import Slider, Button
import matplotlib.pyplot as plt

# TODO: slider

plt.subplots_adjust(left=0.25, bottom=0.25)

axamp = plt.axes([0.1, 0.25, 0.0225, 0.63], facecolor='lightgoldenrodyellow')
amp_slider = Slider(
    ax=axamp,
    label="Amplitude",
    valmin=0,
    valmax=10,
    valinit=5,
    orientation="vertical"
)


def update(val):
    print(val)


amp_slider.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color='lightgoldenrodyellow', hovercolor='0.975')


def reset(event):
    amp_slider.reset()


button.on_clicked(reset)

plt.show()
