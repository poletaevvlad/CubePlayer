from typing import List, Tuple
from math import cos, sin
from ctypes import *

VectorType = Tuple[float, ...]


class Matrix:
    def __init__(self, values: List[List[float]]):
        self.values = values

    def __getitem__(self, item: Tuple[int, int]) -> float:
        return self.values[item[0]][item[1]]

    def __mul__(self, other: "Matrix") -> "Matrix":
        def get_mul_res(i: int, j: int) -> float:
            result = 0.0
            for k in range(4):
                result += self[i, k] * other[k, j]
            return result

        return Matrix([
            [get_mul_res(i, j) for j in range(4)]
            for i in range(4)
        ])

    # noinspection PyCallingNonCallable,PyTypeChecker
    def to_ctypes(self) -> Array:
        array_type = c_float * 16
        flatten = [value for row in self.values for value in row]
        return array_type(*flatten)


def translate(dx: float = 0, dy: float = 0, dz: float = 0) -> Matrix:
    return Matrix([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])


def reflect(x: bool = False, y: bool = False, z: bool = False) -> Matrix:
    return Matrix([
        [-1 if x else 1, 0, 0, 0],
        [0, -1 if y else 1, 0, 0],
        [0, 0, -1 if z else 1, 0],
        [0, 0, 0, 1]
    ])


def rotate_x(angle: float) -> Matrix:
    cos_a = cos(angle)
    sin_a = sin(angle)
    return Matrix([
        [1, 0, 0, 0],
        [0, cos_a, sin_a, 0],
        [0, -sin_a, cos_a, 0],
        [0, 0, 0, 1]
    ])


def rotate_y(angle: float) -> Matrix:
    cos_a = cos(angle)
    sin_a = sin(angle)
    return Matrix([
        [cos_a, 0, -sin_a, 0],
        [0, 1, 0, 0],
        [sin_a, 0, cos_a, 0],
        [0, 0, 0, 1]
    ])


def rotate_z(angle: float) -> Matrix:
    cos_a = cos(angle)
    sin_a = sin(angle)
    return Matrix([
        [cos_a, sin_a, 0, 0],
        [-sin_a, cos_a, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def scale(x: float, y: float, z: float) -> Matrix:
    return Matrix([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ])


def uscale(f: float):
    return scale(f, f, f)


def change_axis(*axis: str) -> Matrix:
    axis_to_index = dict(x=0, y=1, z=2)
    matrix = Matrix([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1]
    ])

    unused = {0, 1, 2}
    for i, x in enumerate(axis):
        j = axis_to_index[x[0]]
        unused.remove(j)
        matrix.values[j][i] = 1 if len(x) == 1 else -1

    for i, j in zip(range(len(axis), 4), unused):
        matrix.values[j][i] = 1
    return matrix


IDENTITY = Matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

C_IDENTITY = IDENTITY.to_ctypes()
