from ..alg.plane_geometry_alg import get_distance_by_tow_point


def get_line_segment_length(line_segment):
    p1 = line_segment.basic_data[0]
    p2 = line_segment.basic_data[1]
    return get_distance_by_tow_point(p1[0], p1[1], p2[0], p2[1])


def attribute_line_segment_length_when_length_change(line_segment):
    line_segment.len = 0

    def inner(line):
        line.len = get_line_segment_length(line)
    line_segment.append_call_back(inner)


def print_line_segment_length_when_length_change(line_segment):
    def inner(line):
        print(get_line_segment_length(line))
    line_segment.append_call_back(inner)


def label_line_segment_length_when_length_change(line_segment):
    def inner(line):
        line.text.set_text(format(get_line_segment_length(line), ".2f"))
    line_segment.append_call_back(inner)
