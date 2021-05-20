from .basic_alg import arctan2, one_degree, sqrt, cos, sin, matmul, arccos, rref, nan


def get_distance_by_tow_point(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def radian2angle(r):
    return r / one_degree


def angle(v1x, v1y, v2x, v2y):
    return arctan2(v1y - v2y, v1x - v2x)


def polar2descartes(r, theta):
    return r * cos(theta), r * sin(theta)


def descartes2polar(x, y):
    return sqrt(x ** 2 + y ** 2), arctan2(y, x)


def polar(geo):
    old_set_data = geo.set_data

    def new_set_data(r, t):
        x, y = polar2descartes(t, r)
        old_set_data(x, y)

    geo.set_data = new_set_data
    geo.update_self()


def get_angle_by_three_point_corr(x1, y1, x2, y2, x3, y3):
    v1 = [x1 - x2, y1 - y2]
    v2 = [x3 - x2, y3 - y2]
    v1_v2 = v1[0] * v2[0] + v1[1] * v2[1]
    v1_len = get_distance_by_tow_point(x1, y1, x2, y2)
    v2_len = get_distance_by_tow_point(x3, y3, x2, y2)
    cos_a = v1_v2 / (v1_len * v2_len)
    a = arccos(cos_a)
    s = v1[0] * v2[1] - v1[1] * v2[0]

    if s > 0:
        return a
    return -a


def get_intersect_point_corr_by_four_point(x1, y1, x2, y2, x3, y3, x4, y4):
    """
    line 1 : (x1, y1), (x2, y2)
    line 2 : (x3, y3), (x4, y4)
    """
    a11 = y2 - y1
    a12 = x1 - x2
    a21 = y4 - y3
    a22 = x3 - x4
    b1 = a11 * x1 + a12 * y1
    b2 = a21 * x3 + a22 * y3
    mat = [
        [a11, a12, b1],
        [a21, a22, b2]
    ]
    mat_simple = rref(mat)
    if mat_simple[1][1] != 0:
        return [mat_simple[0][2], mat_simple[1][2]]
    if mat_simple[1][2] != 0:
        return [nan, nan]
    return [x1, y1]


def get_edge_two_point_by_line(x1, y1, x2, y2, x_min, x_max, y_min, y_max):
    if x1 == x2:
        return [[x1, y_min], [x1, y_max]]

    k = (y1 - y2) / (x1 - x2)
    y1_k_x1 = y1 - k * x1
    y_min = k * x_min + y1_k_x1
    y_max = k * x_max + y1_k_x1

    return [[x_min, y_min], [x_max, y_max]]


def get_abc_by_line(x1, y1, x2, y2):
    if y1 == y2:
        return [0, 1, -y1]
    if x1 == x2:
        return [1, 0, -x1]
    x1_x2 = x1 - x2
    y1_y2 = y1 - y2
    return [y1 - y2, x1 - x2, x1_x2 * y1 - y1_y2 * x1]


def get_middle_point_by_two_point(x1, y1, x2, y2):
    return (x1 + x2) / 2, (y1 + y2) / 2


def get_rotate_point_by_two_point(x1, y1, x2, y2, t):
    x_2_1 = x2 - x1
    y_2_1 = y2 - y1
    return [x1 + x_2_1 * cos(t) - y_2_1 * sin(t),
            y1 + x_2_1 * sin(t) + y_2_1 * cos(t)]


def get_vertical_point_by_point_line(px, py, x1, y1, x2, y2):
    x2_x1 = x2 - x1
    y2_y1 = y2 - y1
    k = ((px - x1) * x2_x1 + (py - y1) * y2_y1) / (x2_x1 ** 2 + y2_y1 ** 2)
    return [x1 + k * x2_x1, y1 + k * y2_y1]


def get_symmetric_point_by_point_line(px, py, x1, y1, x2, y2):
    vp = get_vertical_point_by_point_line(px, py, x1, y1, x2, y2)
    return [2 * vp[0] - px, 2 * vp[1] - py]


def get_symmetric_point_by_point(x1, y1, x2, y2):
    return [2 * x2 - x1, 2 * y2 - y1]


def get_point_by_matrix(mat, x1, y1):
    return matmul(mat, [x1, y1])


def get_transform_vector_to_y_up(x1, y1, x2, y2):
    """
    Move (x1, y1) to positive y-axis become (x3, y3), move (x2, y2) to negative y-axis become (x4, y4),
    and absolute y-coordinate is equal.

    return : [t1, t2]
    t1: [(x3, y3), (x4, y4)] transform to [(x1, y1), (x2, y2)]
    """
    x0, y0 = (x1 + x2) / 2, (y1 + y2) / 2
    delta_x = x1 - x2
    delta_y = y1 - y2
    if delta_x == 0:
        if delta_y == 0:
            return 2 * [lambda x, y: [x, y]]
        if delta_y < 0:
            return [lambda x, y: [-x + x0, -y + y0], lambda x, y: [x0 - x, y0 - y]]
        return [lambda x, y: [x + x0, y + y0], lambda x, y: [x - x0, y - y0]]
    if delta_y == 0:
        if delta_x < 0:
            return [lambda x, y: [-y + x0, x + y0], lambda x, y: [(y - y0), -(x - x0)]]
        return [lambda x, y: [y + x0, -x + y0], lambda x, y: [-(y - y0), (x - x0)]]
    tan_alpha = delta_x / delta_y
    sqrt_1_add_tan2_alpha = sqrt(1 + tan_alpha ** 2)
    if delta_y < 0:
        sqrt_1_add_tan2_alpha = -sqrt_1_add_tan2_alpha
    sin_alpha = tan_alpha / sqrt_1_add_tan2_alpha
    cos_alpha = 1 / sqrt_1_add_tan2_alpha
    return [lambda x, y: [cos_alpha * x + sin_alpha * y + x0, -sin_alpha * x + cos_alpha * y + y0],
            lambda x, y: [cos_alpha * (x - x0) - sin_alpha * (y - y0), sin_alpha * (x - x0) + cos_alpha * (y - y0)]]
