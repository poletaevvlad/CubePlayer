from typing import Tuple, List
from pathlib import Path
from ctypes import Array

from OpenGL.GL import *

from .engine.vbo import load_obj, VAO
from .engine.shaders import Program
from .engine.objects import Object3d, nullptr
from .engine.linalg import (Matrix, translate, change_axis,
                            rotate_x, rotate_y, rotate_z, C_IDENTITY)


class CubePart(Object3d):
    def __init__(self, vao: VAO, material: Program, init_offset: Tuple[float, ...],
                 axis_flip: List[str]):
        super(CubePart, self).__init__(vao, material)
        self.object_transform: Matrix = (translate(*init_offset) *
                                         change_axis(*axis_flip))
        self.temp_rotation: List[float] = [0.0, 0.0, 0.0]

    def set_temp_rotation(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        self.temp_rotation = [x, y, z]

    def apply_temp_rotation(self) -> None:
        rotation = (rotate_x(self.temp_rotation[0]) * rotate_y(self.temp_rotation[1]) *
                    rotate_z(self.temp_rotation[2]))
        self.object_transform = rotation * self.object_transform
        self.temp_rotation = [0, 0, 0]

    def _has_temp_rotation(self) -> bool:
        return any(abs(x) > 1e-5 for x in self.temp_rotation)

    def draw(self, cam_transform: Array, cam_projection: Array) -> None:
        self.material.use()
        glUniformMatrix4fv(self.material.uniforms["cameraTransform"], 1, GL_TRUE, cam_transform)
        glUniformMatrix4fv(self.material.uniforms["cameraProjection"], 1, GL_TRUE, cam_projection)
        glUniformMatrix4fv(self.material.uniforms["objectTransform"], 1, GL_TRUE, self.object_transform.to_ctypes())

        if self._has_temp_rotation():
            rotation = (rotate_x(self.temp_rotation[0]) * rotate_y(self.temp_rotation[1]) *
                        rotate_z(self.temp_rotation[2])).to_ctypes()
        else:
            rotation = C_IDENTITY
        glUniformMatrix4fv(self.material.uniforms["tempTransform"], 1, GL_TRUE, rotation)

        self.vao.bind()
        glDrawElements(GL_TRIANGLES, self.vao.elements_count, GL_UNSIGNED_SHORT, nullptr)


class Cube:
    def __init__(self, shape: Tuple[int, int, int]):
        self.shader = Program("object")
        self.shape: Tuple[int, int, int] = shape

        models_path = Path(__file__).parents[2] / "models"
        self.vao_corner = load_obj(models_path / "corner.obj")
        self.vao_edge = load_obj(models_path / "edge.obj")
        self.vao_flat = load_obj(models_path / "flat.obj")

        self.layers_front: List[List[CubePart]] = [[] for _ in range(self.shape[1])]
        self.layers_top: List[List[CubePart]] = [[] for _ in range(self.shape[2])]
        self.layers_left: List[List[CubePart]] = [[] for _ in range(self.shape[0])]

        self._create_horizontal_end(0)
        for y in range(1, self.shape[1] - 1):
            self._create_vertical_layer(y)
        self._create_horizontal_end(self.shape[1] - 1)

    def _create_part(self, x: int, y: int, z: int, vao_type: VAO) -> None:
        def add_axis(axis_name: str, value: int, max_value: int, result: List[str]) -> None:
            if value == 0:
                result.append(axis_name)
            elif value == max_value - 1:
                result.append(axis_name + "'")

        position = tuple(p - w // 2 + (1 - w % 2) / 2.0 for w, p in zip(self.shape, (x, y, z)))
        axis: List[str] = []
        add_axis("x", x, self.shape[0], axis)
        add_axis("y", y, self.shape[1], axis)
        add_axis("z", z, self.shape[2], axis)

        part = CubePart(vao_type, self.shader, position, axis)
        self.layers_front[y].append(part)
        self.layers_left[x].append(part)
        self.layers_top[z].append(part)

    def _create_horizontal_end(self, y: int) -> None:
        for x in range(self.shape[0]):
            for z in range(self.shape[2]):
                x_corner = x == 0 or x == self.shape[0] - 1
                z_corner = z == 0 or z == self.shape[2] - 1
                shape = self.vao_flat
                if x_corner and z_corner:
                    shape = self.vao_corner
                elif x_corner or z_corner:
                    shape = self.vao_edge
                self._create_part(x, y, z, shape)

    def _create_vertical_layer(self, y: int) -> None:
        for z in {0, self.shape[2] - 1}:
            self._create_part(0, y, z, self.vao_edge)
            self._create_part(self.shape[0] - 1, y, z, self.vao_edge)
            for x in range(1, self.shape[0] - 1):
                self._create_part(x, y, z, self.vao_flat)

        for z in range(1, self.shape[2] - 1):
            self._create_part(0, y, z, self.vao_flat)
            self._create_part(self.shape[0] - 1, y, z, self.vao_flat)

    def draw(self, cam_transform: Array, cam_projection: Array) -> None:
        for layer in self.layers_front:
            for part in layer:
                part.draw(cam_transform, cam_projection)
