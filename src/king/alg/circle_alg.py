from .basic_alg import unit_circle


def get_circle_equation_coefficient_by_center_radius(x1, y1, r):
    return [1, 0, 1, -x1, -y1, x1 ** 2 + y1 ** 2 - r ** 2]


def get_circle_xy_data_by_center_radius(x1, y1, r):
    x_data = r * unit_circle[0]
    y_data = r * unit_circle[1]
    x_data = x_data + x1
    y_data = y_data + y1
    return x_data, y_data
