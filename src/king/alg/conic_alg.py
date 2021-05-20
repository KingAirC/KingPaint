from .basic_alg import sqrt, get_main_element_index_list, real_root_tow_power_equation, det, \
    is_same_negative_or_positive, nan, rref, eig_n, pi_half
from .circle_alg import get_circle_equation_coefficient_by_center_radius
from .plane_geometry_alg import get_rotate_point_by_two_point
from .parabola_alg import get_parabola_equation_coefficient_by_focus_line

CONIC_TYPE_POINT = 0
CONIC_TYPE_LINE = 1
CONIC_TYPE_PARALLEL_LINE = 2
CONIC_TYPE_INTERSECT_LINE = 3
CONIC_TYPE_ELLIPSE = 4
CONIC_TYPE_CIRCLE = 5
CONIC_TYPE_HYPERBOLA = 6
CONIC_TYPE_PARABOLA = 7
CONIC_TYPE_CAN_NOT_PLOT = 8


def elimination_of_cross_phase_by_rotating_shaft(a11, a12, a22, a1, a2, a0):
    """
    a11*x^2 + 2*a12*xy + a22*y^2 + 2a1 * x + 2a2 * y + a0 = 0
    (x, y)' = A * (x2, y2)'
    b11*x2^2 + b22*y2^2 + 2b1 * x2 + 2b2 * y2 + b0 = 0

    return [A, [b11, 0, b22, b1, b2, b0]]
    """
    if a12 == 0:
        mat = [
            [1, 0],
            [0, 1]
        ]
        return mat, [a11, a12, a22, a1, a2, a0]
    delta = (a11 - a22) ** 2 + 4 * a12 ** 2
    sqrt_delta = sqrt(delta)
    sqrt_delta_2 = sqrt_delta / 2
    a11_a22_2 = (a11 + a22) / 2

    eigenvalue_1 = a11_a22_2 + sqrt_delta_2
    eigenvector_1_x = 1
    eigenvector_1_y = (eigenvalue_1 - a11) / a12
    len_1 = sqrt(1 + eigenvector_1_y ** 2)
    eigenvector_1_x /= len_1
    eigenvector_1_y /= len_1

    eigenvalue_2 = a11_a22_2 - sqrt_delta_2
    eigenvector_2_x = 1
    eigenvector_2_y = (eigenvalue_2 - a11) / a12
    len_2 = sqrt(1 + eigenvector_2_y ** 2)
    eigenvector_2_x /= len_2
    eigenvector_2_y /= len_2

    mat = [
        [eigenvector_1_x, eigenvector_2_x],
        [eigenvector_1_y, eigenvector_2_y]
    ]
    b1 = a1 * eigenvector_1_x + a2 * eigenvector_1_y
    b2 = a1 * eigenvector_2_x + a2 * eigenvector_2_y

    return mat, [eigenvalue_1, 0, eigenvalue_2, b1, b2, a0]


def shift_axis(a11, a12, a22, a1, a2, a0):
    """
    a11*x^2 + a22*y^2 + 2a1 * x + 2a2 * y + a0 = 0
    (x, y)' = (x2, y2)' + B
    b11*x2^2 + b22*y2^2 + 2b1 * x2 + 2b2 * y2 + b0 = 0

    return [B, [b11, 0, b22, b1, b2, b0]]
    """
    if a11 != 0:
        if a22 != 0:
            return [[a1 / a11, a2 / a22], [a11, 0, a22, 0, 0, a0 - a1 ** 2 / a11 - a2 ** 2 / a22]]
        if a2 == 0:
            return [[a1 / a11, 0], [a11, 0, 0, 0, 0, a0 - a1 ** 2 / a11]]
        return [[a1 / a11, (a0 - a1 ** 2 / a11) / (2 * a2)], [a11, 0, 0, 0, a2, 0]]
    if a22 != 0:
        if a1 == 0:
            return [[0, a2 / a22], [0, 0, a22, 0, 0, a0 - a2 ** 2 / a22]]
        return [[(a0 - a2 ** 2 / a22) / (2 * a1), a2 / a22], [0, 0, a22, a1, 0, 0]]
    return [[0, 0], [0, 0, 0, a1, a2, a0]]


def get_simplest_conic_equation_and_transform_by_conic_equation(a11, a12, a22, a1, a2, a0):
    """
    a11*x^2 + 2*a12*xy + a22*y^2 + 2a1 * x + 2a2 * y + a0 = 0

    X1 = (x1, y1)'
    X2 = (x2, y2)'
    X3 = (x3, y3)'

    X1 = A * X2
    X3 = B + X2

    return [t1, t2, [c11, c12, c22, c1, c2, c0]]
    t1 : X3 -> X1 : X1 = A * (X3 - B)
    t2 : X1 -> X3 : X3 = A^(-1) * X1 + B
    """
    rotate_mat, rotate_coefficient = elimination_of_cross_phase_by_rotating_shaft(a11, a12, a22, a1, a2, a0)
    translation_mat, translation_coefficient = shift_axis(*rotate_coefficient)

    def t1(x, y):
        x_translation_mat_0 = x - translation_mat[0]
        y_translation_mat_1 = y - translation_mat[1]
        return [rotate_mat[0][0] * x_translation_mat_0 + rotate_mat[0][1] * y_translation_mat_1,
                rotate_mat[1][0] * x_translation_mat_0 + rotate_mat[1][1] * y_translation_mat_1]

    def t2(x, y):
        return [rotate_mat[0][0] * x + rotate_mat[1][0] * y + translation_mat[0],
                rotate_mat[0][1] * x + rotate_mat[1][1] * y + translation_mat[1]]

    return [t1, t2, translation_coefficient]


def get_conic_type_and_basic_data_by_simplest_equation(a11, a12, a22, a1, a2, a0):
    """
    get conic type and basic data by simplest equation.

    return [type, basic_data]
    """
    if a11 < 0:
        a11 = -a11
        a22 = -a22
        a0 = -a0
    if a11 > 0:
        if a22 > 0:
            if a0 < 0:
                if a11 < a22:
                    cc = (1 / a22 - 1 / a11) * a0
                    c = sqrt(cc)
                    return [CONIC_TYPE_ELLIPSE, [[c, 0], [-c, 0], 2 * sqrt(-a0 / a11)]]
                elif a11 == a22:
                    return [CONIC_TYPE_CIRCLE, sqrt(-a0 / a11)]
                else:
                    cc = (1 / a11 - 1 / a22) * a0
                    c = sqrt(cc)
                    return [CONIC_TYPE_ELLIPSE, [[0, c], [0, -c], 2 * sqrt(-a0 / a22)]]
            elif a0 > 0:
                return [CONIC_TYPE_CAN_NOT_PLOT]
            else:
                # (0, 0)
                return [CONIC_TYPE_POINT]
        elif a22 < 0:
            if a0 == 0:
                k = sqrt(-a11 / a22)
                return [CONIC_TYPE_INTERSECT_LINE, [[[0, 0], [1, k]], [[0, 0], [1, -k]]]]
            elif a0 > 0:
                cc = (1 / a11 - 1 / a22) * a0
                c = sqrt(cc)
                return [CONIC_TYPE_HYPERBOLA, [[0, c], [0, -c], 2 * sqrt(-a0 / a22)]]
            else:
                cc = (1 / a22 - 1 / a11) * a0
                c = sqrt(cc)
                return [CONIC_TYPE_HYPERBOLA, [[c, 0], [-c, 0], 2 * sqrt(-a0 / a11)]]
        else:
            if a2 == 0:
                if a0 > 0:
                    return [CONIC_TYPE_CAN_NOT_PLOT]
                elif a0 < 0:
                    x = sqrt(-a0 / a11)
                    return [CONIC_TYPE_PARALLEL_LINE, [[[x, 0], [x, 1]], [[-x, 0], [-x, 1]]]]
                else:
                    return [CONIC_TYPE_LINE, [[0, 0], [0, 1]]]
            else:
                return [CONIC_TYPE_PARABOLA, [[0, -(a0 / a2 + a2 / a11) / 2], [0, (a2 / a11 - a0 / a2) / 2]]]
    else:
        if a22 == 0:
            if a1 == 0:
                return [CONIC_TYPE_CAN_NOT_PLOT]
            x = -a0 / (2 * a1)
            return [CONIC_TYPE_LINE, [[x, 0], [x, 1]]]
        if a22 < 0:
            a22 = -a22
            a1 = -a1
            a0 = -a0
        if a22 > 0:
            if a1 == 0:
                if a0 == 0:
                    return [CONIC_TYPE_LINE, [[0, 0], [1, 0]]]
                elif a0 > 0:
                    return [CONIC_TYPE_CAN_NOT_PLOT]
                else:
                    y = sqrt(-a0 / a22)
                    return [CONIC_TYPE_PARALLEL_LINE, [[[0, y], [1, y]], [[0, -y], [1, -y]]]]
            else:
                return [CONIC_TYPE_PARABOLA, [[-(a1 / a22 + a0 / a1) / 2, 0], [(a1 / a22 - a0 / a1) / 2, 0]]]


def get_conic_mat_by_five_point(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5):
    """
    a11 * x^2 + 2a12 * xy + a22 * y^2 + 2a1 * x + 2a2 * y + a0 = 0
    """

    def row(x, y):
        return [x ** 2, 2 * x * y, y ** 2, 2 * x, 2 * y, 1]

    return [row(*point) for point in zip([x1, x2, x3, x4, x5], [y1, y2, y3, y4, y5])]


def get_conic_coefficient(row_simplest_matrix):
    """
    Parameter
    =========
    row simplest matrix represent for 5 point conic's equation.

    return: A list which elements is: [a11, a12, a22, a1, a2, a0]
    """
    index_list = get_main_element_index_list(row_simplest_matrix)
    rank = len(index_list)
    if rank == 5:
        i = 0
        flag = True
        while i < rank - 1:
            if index_list[i + 1] - index_list[i] > 1:
                i += 1
                flag = False
                break
            i += 1
        if flag:
            i = rank
        result = [row_simplest_matrix[j][i] for j in range(i)]
        result.append(-1)
        result.extend([0] * (rank - i))
        return result
    # TODO : case rank < 5


def get_central_conic_equation_coefficient_by_focus_d(x1, y1, x2, y2, d):
    """
    central conic include ellipse, circle, hyperbola.
    especially ellipse and hyperbola.
    when ellipse, assign two focus and add.
    when hyperbola, assign two focus and difference.
    """
    dd = d * d
    dddd = dd * dd
    x1x1 = x1 * x1
    x2x2 = x2 * x2
    y1y1 = y1 * y1
    y2y2 = y2 * y2
    x1x1x1x1 = x1x1 * x1x1
    x2x2x2x2 = x2x2 * x2x2
    y1y1y1y1 = y1y1 * y1y1
    y2y2y2y2 = y2y2 * y2y2
    x1_x2 = x1 - x2
    y1_y2 = y1 - y2
    x1_add_x2 = x1 + x2
    y1_add_y2 = y1 + y2
    x1_x2_2 = x1_x2 * x1_x2
    y1_y2_2 = y1_y2 * y1_y2
    a11 = 4 * (x1_x2_2 - dd)
    a22 = 4 * (y1_y2_2 - dd)
    a12 = 4 * x1_x2 * y1_y2
    a1 = 2 * (dd * x1_add_x2 - x1_add_x2 * x1_x2_2 - x1_x2 * y1_add_y2 * y1_y2)
    a2 = 2 * (dd * y1_add_y2 - y1_add_y2 * y1_y2_2 - y1_y2 * x1_add_x2 * x1_x2)
    a0 = x1x1x1x1 - 2 * x1x1 * x2x2 + 2 * x1x1 * y1y1 - 2 * x1x1 * y2y2 + x2x2x2x2 - 2 * x2x2 * y1y1 + 2 * x2x2 * y2y2 + y1y1y1y1 - 2 * y1y1 * y2y2 + y2y2y2y2 + dddd - 2 * dd * x1x1 - 2 * dd * x2x2 - 2 * dd * y1y1 - 2 * dd * y2y2

    return [a11, a12, a22, a1, a2, a0]


def get_conic_value_by_point(x0, y0, a11, a12, a22, a1, a2, a0):
    return a11 * x0 ** 2 + 2 * a12 * x0 * y0 + a22 * y0 ** 2 + 2 * a1 * x0 + 2 * a2 * y0 + a0


def get_conic_I1(a11, a12, a22, a1, a2, a0):
    return a11 + a22


def get_conic_I2(a11, a12, a22, a1, a2, a0):
    return a11 * a22 - a12 ** 2


def get_conic_I3(a11, a12, a22, a1, a2, a0):
    mat = [
        [a11, a12, a1],
        [a12, a22, a2],
        [a1, a2, a0]
    ]
    return det(mat)


def get_conic_K1(a11, a12, a22, a1, a2, a0):
    return a0 * (a11 + a22) - a1 ** 2 - a2 ** 2


def get_conic_type_simply_equation(a11, a12, a22, a1, a2, a0):
    I1 = get_conic_I1(a11, a12, a22, a1, a2, a0)
    I2 = get_conic_I2(a11, a12, a22, a1, a2, a0)
    I3 = get_conic_I3(a11, a12, a22, a1, a2, a0)

    if I2 > 0:
        same_symbol = is_same_negative_or_positive(I1, I3)
        if same_symbol is not None:
            return [CONIC_TYPE_CAN_NOT_PLOT]
        if I3 == 0:
            return [CONIC_TYPE_POINT]
        roots = real_root_tow_power_equation(1, -I1, I2)
        if len(roots) == 1:
            return [CONIC_TYPE_CIRCLE, [1, 0, 1, 0, 0, I3 / I2 / roots[0]]]
        return [CONIC_TYPE_ELLIPSE, [roots[0], 0, roots[1], 0, 0, I3 / I2]]
    if I2 < 0:
        roots = real_root_tow_power_equation(1, -I1, I2)
        root_1 = roots[0]
        root_2 = root_1 if len(roots) == 1 else roots[1]
        corr = [root_1, 0, root_2, 0, 0, I3 / I2]
        conic_type = CONIC_TYPE_INTERSECT_LINE if I3 == 0 else CONIC_TYPE_HYPERBOLA
        return [conic_type, corr]
    if I3 == 0:
        K1 = get_conic_K1(a11, a12, a22, a1, a2, a0)
        if K1 < 0:
            return [CONIC_TYPE_PARALLEL_LINE, [0, 0, 1, 0, 0, K1 / (I1 ** 2)]]
        if K1 > 0:
            return [CONIC_TYPE_CAN_NOT_PLOT]
        return [CONIC_TYPE_LINE, [0, 0, 1, 0, 0, 0]]
    return [CONIC_TYPE_PARABOLA, [0, 0, I1, 2 * (-I3 / I1) ** (1 / 2), 0, 0]]


def intersect_line_conic(x1, y1, x2, y2, a11, a12, a22, a1, a2, a0):
    vx, vy = x2 - x1, y2 - y1
    at2 = a11 * vx ** 2 + 2 * a12 * vx * vy + a22 * vy ** 2
    f1x1y1 = a11 * x1 + a12 * y1 + a1
    f2x1y1 = a12 * x1 + a22 * y1 + a2
    at1 = 2 * (f1x1y1 * vx + f2x1y1 * vy)
    at0 = a11 * x1 ** 2 + 2 * a12 * x1 * y1 + a22 * y1 ** 2 + 2 * a1 * x1 + 2 * a2 * y1 + a0

    roots = real_root_tow_power_equation(at2, at1, at0)

    if roots is None:
        return None

    def get_xy_by_t(t):
        return [x1 + t * vx, y1 + t * vy]

    if len(roots) == 1:
        return [get_xy_by_t(roots[0])]

    return get_xy_by_t(roots[0]), get_xy_by_t(roots[1])


def get_conic_symmetry_center(a11, a12, a22, a1, a2, a0):
    mat = [
        [a11, a12, -a1],
        [a12, a22, -a2]
    ]
    mat2 = rref(mat)
    if mat2[1][1] != 0:
        return mat2[0][2], mat2[1][2]
    return None


def get_conic_asymptote_vector(a11, a12, a22, a1, a2, a0):
    roots = real_root_tow_power_equation(a22, 2 * a12, a11)

    return roots


def get_diameter_direction_by_conic(a11, a12, a22, a1, a2, a0):
    mat = [
        [a11, a12],
        [a12, a22]
    ]

    return eig_n(mat)


def get_coefficient_by_conic(conic):
    conic_type = conic.conic_type_cls_var
    if conic_type is None:
        coe = conic.basic_data
    elif conic_type == CONIC_TYPE_CIRCLE:
        coe = get_circle_equation_coefficient_by_center_radius(*conic.basic_data[0], conic.basic_data[1])
    elif conic_type == CONIC_TYPE_ELLIPSE or conic_type == CONIC_TYPE_HYPERBOLA:
        x1, y1 = conic.basic_data[0]
        x2, y2 = conic.basic_data[1]
        d = conic.basic_data[2]
        coe = get_central_conic_equation_coefficient_by_focus_d(x1, y1, x2, y2, d)
    elif conic_type == CONIC_TYPE_PARABOLA:
        xp, yp = conic.basic_data[0]
        xv, yv = conic.basic_data[1]
        x2, y2 = get_rotate_point_by_two_point(xv, yv, xp, yp, pi_half)
        coe = get_parabola_equation_coefficient_by_focus_line(xp, yp, xv, yv, x2, y2)
    else:
        coe = None
    return coe


def conic_tangent_vector(x0, y0, a11, a12, a22, a1, a2, a0):
    fx0y0 = get_conic_value_by_point(x0, y0, a11, a12, a22, a1, a2, a0)
    f1x0y0 = a11 * x0 + a12 * y0 + a1
    f2x0y0 = a12 * x0 + a22 * y0 + a2
    if fx0y0 == 0:
        x = -f2x0y0
        y = f1x0y0
        return [[x, y]]

    def fi(u, v):
        return a11 * u ** 2 + 2 * a12 * u * v + a22 * v ** 2

    cu = f1x0y0 ** 2 - fx0y0 * a11
    cuv = f1x0y0 * f2x0y0 - fx0y0 * a12
    cv = f2x0y0 ** 2 - fx0y0 * a22
    res = []
    if cv != 0:
        roots = real_root_tow_power_equation(cv, 2 * cuv, cu)
        if roots is None:
            return
        if len(roots) == 1:
            fii = fi(1, roots[0])
            if fii != 0:
                res.append([1, roots[0], -(f1x0y0 + roots[0] * f2x0y0) / fii])
                return res
        fii1 = fi(1, roots[0])
        if fii1 != 0:
            res.append([1, roots[0], -(f1x0y0 + roots[0] * f2x0y0) / fii1])
        fii2 = fi(1, roots[1])
        if fii2 != 0:
            res.append([1, roots[1], -(f1x0y0 + roots[1] * f2x0y0) / fii2])
        return res
    if cuv != 0:
        fii1 = fi(0, 1)
        if fii1 != 0:
            res.append([0, 1, -f2x0y0 / fii1])
        fii2 = fi(-2 * cuv, cu)
        if fii2 != 0:
            res.append([-2 * cuv, cu, -(-2 * cuv * f1x0y0 + cu * f2x0y0) / fii2])
        return res
    return
