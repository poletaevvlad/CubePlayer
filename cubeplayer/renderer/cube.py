from ctypes import Array
from pathlib import Path
from typing import Tuple, List

from OpenGL.GL import *

from libcube.cube import Cube as CubeModel
from libcube.orientation import Orientation
from .engine.linalg import (Matrix, translate, change_axis,
                            rotate_x, rotate_y, rotate_z, C_IDENTITY)
from .engine.objects import Object3d, nullptr
from .engine.shaders import Program
from .engine.vbo import load_obj, VAO
from .engine.light import DirectionalLight


class CubePart(Object3d):
    LIGHTS: List[DirectionalLight] = [
        DirectionalLight((1.0, 0.5, 0.5), (1.0, 1.0, 1.0)),
        DirectionalLight((0.5, 0.5, 1.0), (-1.0, 0.0, 1.0))
    ]

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
        self.cube: CubeModel[CubePart] = CubeModel[CubePart](shape)

        self.shader = Program("object")
        self.shader.use()
        DirectionalLight.push_uniform_array(self.shader, "lights", CubePart.LIGHTS)

        models_path = Path(__file__).parents[2] / "models"
        self.vao_corner = load_obj(models_path / "corner.obj")
        self.vao_edge = load_obj(models_path / "edge.obj")
        self.vao_flat = load_obj(models_path / "flat.obj")

        self.parts: List[CubePart] = []

        for side, i, j in self.cube.iterate_components():
            x, y, z = self.cube.get_absolute_coordinates(side, i, j)
            y = self.cube.shape[2] - 1 - y
            z = self.cube.shape[1] - 1 - z

            part = self._create_part(x, y, z)
            self.parts.append(part)
            self.cube.set_data(Orientation.regular(side), i, j, part)

    def _create_part(self, x: int, y: int, z: int) -> CubePart:
        num_corners = 0

        def add_axis(axis_name: str, value: int, max_value: int, result: List[str]) -> None:
            nonlocal num_corners
            if value == 0:
                result.append(axis_name)
                num_corners += 1
            elif value == max_value - 1:
                result.append(axis_name + "'")
                num_corners += 1

        position = tuple(p - w // 2 + (1 - w % 2) / 2.0 for w, p in zip(self.cube.shape, (x, y, z)))
        axis: List[str] = []
        add_axis("x", x, self.cube.shape[0], axis)
        add_axis("y", y, self.cube.shape[2], axis)
        add_axis("z", z, self.cube.shape[1], axis)

        vao = self.vao_flat if num_corners == 0 else self.vao_edge if num_corners == 1 else self.vao_corner
        part = CubePart(vao, self.shader, position, axis)
        return part

    def draw(self, cam_transform: Array, cam_projection: Array) -> None:
        for part in self.parts:
            part.draw(cam_transform, cam_projection)