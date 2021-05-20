"""
support numeric calculate and symbolic calculate.
can choose which type of function to invoke automatically.
symbolic calculate must pass sympy object and return sympy object.
"""

import numpy as np
import ctypes
import sympy
import platform
import random

pi = np.pi
pi_half = pi / 2
pi_one_third = pi / 3
pi_quarter = pi / 4
one_degree = pi / 180
pi_2 = pi * 2
theta_list = np.linspace(0, pi_2, 360)
theta_list.flags.writeable = False
unit_circle = (np.cos(theta_list), np.sin(theta_list))
unit_circle[0].flags.writeable = False
unit_circle[1].flags.writeable = False
nan = np.nan
libc = None
sys_type = platform.system()
tow_empty_line_basic_data = [[[nan] * 2] * 2] * 2
empty_line_basic_data = [[nan] * 2] * 2
empty_point_basic_data = [nan, nan]

try:
    lib_location = None
    if sys_type == "Windows":
        lib_location = '../../../Clib/bin/libKingAlg.dll'
    elif sys_type == "Linux":
        lib_location = '../../../Clib/bin/libKingAlg.so'
    libc = ctypes.cdll.LoadLibrary(lib_location)
except OSError:
    libc = None
    print(OSError)


def is_zero(n):
    return abs(n) < 0.1e-7


def transfer_sympy_matrix_to_array(matrix):
    row = matrix.rows
    col = matrix.cols
    result = []

    for i in range(row):
        result.append([])
        for j in range(col):
            result[i].append(matrix[i * col + j])

    return result


def array(p_object):
    return np.array(p_object)


def linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0):
    return np.linspace(start, stop, num=num, endpoint=endpoint, retstep=retstep, dtype=dtype, axis=axis)


def is_sympy_object(o):
    if isinstance(o, sympy.Symbol):
        return True
    if isinstance(o, sympy.Integer):
        return True
    if isinstance(o, sympy.Matrix):
        return True
    if isinstance(o, sympy.Rational):
        return True
    return False


def cos_n(t):
    return np.cos(t)


def cos_s(t):
    return sympy.cos(t)


def cos(t):
    if is_sympy_object(t):
        return cos_s(t)
    return cos_n(t)


def arccos_n(t):
    return np.arccos(t)


def arccos_s(t):
    return sympy.acos(t)


def arccos(t):
    if is_sympy_object(t):
        return arccos_s(t)
    return arccos_n(t)


def sin_n(t):
    return np.sin(t)


def sin_s(t):
    return sympy.sin(t)


def sin(t):
    if is_sympy_object(t):
        return sin_s(t)
    return sin_n(t)


def arctan2_n(x1, x2):
    return np.arctan2(x1, x2)


def arctan2_s(x1, x2):
    return sympy.atan2(x1, x2)


def arctan2(x1, x2):
    if is_sympy_object(x1) or is_sympy_object(x2):
        return arctan2_s(x1, x2)
    return arctan2_n(x1, x2)


def sqrt_n(x):
    return np.sqrt(x)


def sqrt_s(x):
    return sympy.sqrt(x)


def sqrt(x):
    if is_sympy_object(x):
        return sqrt_s(x)
    return sqrt_n(x)


def matmul_n(x1, x2):
    return np.matmul(x1, x2)


def matmul_s(x1, x2):
    if not is_sympy_object(x1):
        x1 = sympy.Matrix(x1)
    if not is_sympy_object(x2):
        x2 = sympy.Matrix(x2)
    return x1 * x2


def matmul(x1, x2):
    if is_sympy_object(x1) or is_sympy_object(x2):
        return matmul_s(x1, x2)
    return matmul_n(x1, x2)


def rref_s(mat):
    return mat.rref(pivots=False)


def rref_n(mat):
    c_rref = libc.rref
    c_rref.restype = None

    row = len(mat)
    col = len(mat[0])

    result = ((ctypes.c_double * col) * row)()

    for i in range(row):
        for j in range(col):
            result[i][j] = ctypes.c_double(mat[i][j])

    c_rref(row, col, result)

    return result


def rref(mat):
    if is_sympy_object(mat):
        return rref_s(mat)
    if libc is None:
        sympy_mat = rref_s(sympy.Matrix(mat))
        arr = transfer_sympy_matrix_to_array(sympy_mat)
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                arr[i][j] = float(arr[i][j])
        return arr
    return rref_n(mat)


def get_main_element_index_list_s(row_simplest_matrix):
    result = []
    row = row_simplest_matrix.rows
    col = row_simplest_matrix.cols
    i = 0
    j = 0
    while i < row:
        while j < col:
            if row_simplest_matrix[i * col + j] != 0:
                result.append(j)
                j += 1
                break
            j += 1
        if j == col:
            return result
        i += 1
    return result


def get_main_element_index_list_n(row_simplest_matrix):
    result = []
    row = len(row_simplest_matrix)
    col = len(row_simplest_matrix[0])
    i = 0
    j = 0
    while i < row:
        while j < col:
            if row_simplest_matrix[i][j] != 0:
                result.append(j)
                j += 1
                break
            j += 1
        if j == col:
            return result
        i += 1
    return result


def random_color_number():
    n = hex(random.randint(0, 255))[2:]
    if len(n) == 1:
        return '0' + n
    return n


def random_color():
    return '#' + random_color_number() + random_color_number() + random_color_number()


def get_main_element_index_list(row_simplest_matrix):
    if is_sympy_object(row_simplest_matrix):
        return get_main_element_index_list_s(row_simplest_matrix)
    return get_main_element_index_list_n(row_simplest_matrix)


def eig_n(mat):
    m = np.array(mat)
    eig = np.linalg.eig(m)

    return [[eig[1][0][0], eig[1][1][0]], [eig[1][0][1], eig[1][1][1]], [eig[0][0], eig[0][1]]]


def det(mat):
    if is_sympy_object(mat):
        return sympy.det(mat)
    if not isinstance(mat, np.ndarray):
        mat = np.array(mat)
    return np.linalg.det(mat)


def trace(mat):
    if is_sympy_object(mat):
        return mat.trace()
    if not isinstance(mat, np.ndarray):
        mat = np.array(mat)
    return mat.trace()


def real_root_tow_power_equation(a, b, c):
    """
    ax^2+bx+c=0
    """
    delta = b ** 2 - 4 * a * c
    if abs(delta) < 0.1e-7:
        delta = 0
    if delta < 0:
        return None
    if delta == 0:
        return [-b / (2 * a)]
    sqrt_delta = sqrt(delta)
    a2 = 2 * a
    a2_b = -b / a2
    return [a2_b - sqrt_delta / a2, a2_b + sqrt_delta / a2]


def is_same_negative_or_positive(x1, x2):
    if x1 > 0 and x2 > 0:
        return 1
    if x1 < 0 and x2 < 0:
        return -1
    if x1 == 0 and x2 == 0:
        return 0
    return None


def is_object_in_class_list(o, cls_list):
    for i in cls_list:
        if isinstance(o, i):
            return True
    return False


def get_xy_data_near_curve(x, y, x_data, y_data, epsilon):
    # TODO: get_xy_data_near_curve
    return
