from ..alg.plane_geometry_alg import get_angle_by_three_point_corr


def get_angle_by_three_point(p1, p2, p3):
    return get_angle_by_three_point_corr(*p1.basic_data, *p2.basic_data, *p3.basic_data)


def print_angle_by_three_point_when_change(p1, p2, p3):
    p1.append_call_back(lambda point_1: print(get_angle_by_three_point(point_1, p2, p3)))
    p2.append_call_back(lambda point_2: print(get_angle_by_three_point(p1, point_2, p3)))
    p3.append_call_back(lambda point_3: print(get_angle_by_three_point(p1, p2, point_3)))


def label_angle_by_three_point_when_change(p1, p2, p3):

    def inner1(point):
        p2.text.set_text(format(get_angle_by_three_point(point, p2, p3), ".2f"))

    def inner2(point):
        p2.text.set_text(format(get_angle_by_three_point(p1, point, p3), ".2f"))

    def inner3(point):
        p2.text.set_text(format(get_angle_by_three_point(p1, p2, point), ".2f"))

    p1.append_call_back(inner1)
    p2.append_call_back(inner2)
    p3.append_call_back(inner3)
