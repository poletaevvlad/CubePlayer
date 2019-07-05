from typing import Tuple, List
from math import radians, tan
from .linalg import Matrix, rotate_x, rotate_y, rotate_z, translate, uscale

Coordinate = Tuple[float, float, float]
ORIGIN: Coordinate = (0.0, 0.0, 0.0)


class Camera:
    def __init__(self, center: Coordinate = ORIGIN, rotation: Coordinate = ORIGIN,
                 offset_value: float = 10, horizontal_fov: float = radians(90),
                 far: float = 50.0, near: float = 0.1, scale: float = 1):
        self.scale: float = scale
        self.center: List[float] = list(center)
        self.rotation: List[float] = list(rotation)
        self.offset_value: float = offset_value
        self.horizontal_fov: float = horizontal_fov# / scale
        self.far: float = far
        self.near: float = near

    def position_transform(self) -> Matrix:
        rotate = uscale(self.scale) * rotate_z(self.rotation[2]) * rotate_x(self.rotation[0]) * \
                 rotate_y(self.rotation[1])
        return translate(0, 0, -self.offset_value) * rotate

    def perspective_transform(self, width: int, height: int) -> Matrix:
        aspect_ratio = float(width) / float(height)

        right = tan(self.horizontal_fov / 2) * self.near
        left = -right

        top = right / aspect_ratio
        bottom = -top

        return Matrix([
            [2 * self.near / (right - left), 0, (right + left) / (right - left), 0],
            [0, 2 * self.near / (top - bottom), (top + bottom) / (top - bottom), 0],
            [0, 0, -(self.far + self.near) / (self.far - self.near),
                -2 * self.far * self.near / (self.far - self.near)],
            [0, 0, -1, 0]
        ])
