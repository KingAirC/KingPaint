def affine(curve, trans):
    def f(s):
        new_x_data, new_y_data = trans(curve.get_xdata(), curve.get_ydata())
        curve.set_data(new_x_data, new_y_data)
    curve.append_call_back(f)
