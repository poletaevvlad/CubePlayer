from typing import List, Tuple, Union
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

    # def mul_vector(self, vector: VectorType) -> VectorType:
    #     def get_mul_result(i: int) -> float:
    #         result = 0.0
    #         for j in range(4):
    #             result += vector[j] * self[i, j]
    #         return result
    #
    #     return tuple(get_mul_result(x) for x in range(4))

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


def mirror(x: bool = False, y: bool = False, z: bool = False) -> Matrix:
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
