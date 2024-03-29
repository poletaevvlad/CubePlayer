from ctypes import Array
from pathlib import Path
from typing import Tuple, List, Dict, Optional

from OpenGL.GL import *

from cubelang.cube import Cube as CubeModel
from cubelang.orientation import Orientation, Color, Side
from .label import Label
from .engine.linalg import Matrix, translate, change_axis, C_IDENTITY, IDENTITY
from .engine.objects import Object3d
from .engine.shaders import Program
from .engine.vbo import load_obj, VAO
from .engine.light import DirectionalLight
from .engine.texture import Texture
from .engine.linalg import rotate_x, rotate_y, rotate_z


class CubePart(Object3d):
    LIGHTS: List[DirectionalLight] = [
        DirectionalLight((255.0 / 255.0, 214.0 / 255.0, 170.0 / 255.0), 0.9, (1.0, 1.0, 3.0)),
        DirectionalLight((170.0 / 255.0, 214.0 / 255.0, 255.0 / 255.0), 0.5, (-1.0, 0.0, 1.0))
    ]

    LABEL_ROTATIONS = {
        Side.FRONT:  [[(-4, 0), (-3, 1), (0, 0)], [(-2, 1), (1, 0), (2, 1)], [(2, 0), (1, 1), (-2, 0)]],
        Side.LEFT:   [[(0, 1), (3, 0), (-4, 1)], [(0, 0), (-2, 0), (-4, 0)], [(-2, 1), (-1, 0), (2, 1)]],
        Side.RIGHT:  [[(0, 1), (-3, 0), (-4, 1)], [(0, 0), (2, 0), (-4, 0)], [(-2, 1), (1, 0), (2, 1)]],
        Side.BACK:   [[(-4, 0), (3, 1), (0, 0)], [(-2, 1), (-1, 0), (2, 1)], [(2, 0), (-1, 1), (-2, 0)]],
        Side.TOP:    [[(2, 2), (3, 0), (-2, 2)], [(0, 1), (-3, 0), (-4, 1)], [(-4, 2), (-1, 0), (0, 2)]],
        Side.BOTTOM: [[(2, 2), (3, 0), (-2, 2)], [(-2, 1), (1, 0), (2, 1)], [(-4, 2), (-1, 0), (0, 2)]]
    }

    def __init__(self, vao: VAO,
                 material: Program,
                 init_offset: Tuple[float, ...],
                 axis_flip: List[str],
                 colors: List[Color],
                 theme: Dict[Color, Tuple[float, float, float]]):
        super(CubePart, self).__init__(vao, material)
        self.object_transform: Matrix = (translate(*init_offset) *
                                         change_axis(*axis_flip))
        self.temp_rotation: List[float] = [0.0, 0.0, 0.0]
        self.colors: List[Color] = colors
        self.label_rotation = 0
        self.label_visible = -1
        self.theme = theme

    def set_temp_rotation(self, x: float = 0, y: float = 0, z: float = 0) -> None:
        self.temp_rotation = [x, y, z]

    def apply_temp_rotation(self) -> None:
        rotation = (rotate_x(self.temp_rotation[0]) * rotate_y(self.temp_rotation[1]) *
                    rotate_z(self.temp_rotation[2]))
        self.object_transform = rotation * self.object_transform
        self.temp_rotation = [0, 0, 0]

    def draw(self) -> None:
        glUniformMatrix4fv(self.material.uniforms["objectTransform"], 1, GL_TRUE, self.object_transform.to_ctypes())
        if any(abs(x) > 1e-5 for x in self.temp_rotation):
            rotation = (rotate_x(self.temp_rotation[0]) * rotate_y(self.temp_rotation[1]) *
                        rotate_z(self.temp_rotation[2])).to_ctypes()
        else:
            rotation = C_IDENTITY
        glUniformMatrix4fv(self.material.uniforms["tempTransform"], 1, GL_TRUE, rotation)
        glUniform1f(self.material.uniforms["label_rotation"], self.label_rotation)
        glUniform3f(self.material.uniforms["label_color_visibility"],
                    *[1 if i == self.label_visible else 0 for i in range(3)])

        for i, color in enumerate(self.colors):
            glUniform3f(self.material.uniforms["colors", i], *self.theme[color])
        self.vao.draw()


class Cube:
    def __init__(self, cube: CubeModel[CubePart], label: Optional[Label],
                 color_theme: Dict[Color, Tuple[float, float, float]]):
        self.cube: CubeModel[CubePart] = cube
        self.label = label
        self.color_theme = color_theme

        self.shader = Program("object")
        self.shader.use()
        DirectionalLight.push_uniform_array(self.shader, "lights", CubePart.LIGHTS)

        models_path = Path(__file__).parents[1] / "models"
        self.vao_corner = load_obj(models_path / "corner.obj")
        self.vao_edge = load_obj(models_path / "edge.obj")
        self.vao_flat = load_obj(models_path / "flat.obj")
        self.stickers_texture = Texture.load("stickers", flip=True, mipmap=True)
        self.labels_texture = Texture.load("labels", flip=True, mipmap=True)

        self.parts: List[CubePart] = self._generate()

        if self.label is not None:
            orientation = Orientation.regular(self.label.side)
            side = self.cube.get_side(orientation)
            row, column = self.label.row, self.label.column

            rot_i = 0 if row == 0 else 2 if row == side.rows - 1 else 1
            rot_j = 0 if column == 0 else 2 if column == side.columns - 1 else 1
            part = side[row, column].data
            rotation, color = CubePart.LABEL_ROTATIONS[self.label.side][rot_i][rot_j]
            part.label_rotation = rotation
            part.label_visible = color

        self.rotation = IDENTITY
        self.temp_rotation = [0, 0, 0]

    def _get_colors(self, side: Side, i: int, j: int) -> List[Color]:
        orientation = Orientation.regular(side)
        front_side = self.cube.get_side(orientation)
        colors = [front_side.colors[i, j]]
        if i == 0 or i == front_side.rows - 1:
            if i == 0:
                top_side = self.cube.get_side(orientation.to_top)
                color = top_side.colors[top_side.rows - 1, j]
            else:
                bottom_side = self.cube.get_side(orientation.to_bottom)
                color = bottom_side.colors[0, j]
            colors.insert(0 if side in {Side.FRONT, Side.BACK} else 1, color)

        if j == 0 or j == front_side.columns - 1:
            if j == 0:
                left_side = self.cube.get_side(orientation.to_left)
                color = left_side.colors[i, left_side.columns - 1]
            else:
                right_side = self.cube.get_side(orientation.to_right)
                color = right_side.colors[i, 0]
            colors.insert(0, color)

        if len(colors) == 3:
            return [colors[2], colors[0], colors[1]]
        return colors

    def _generate(self) -> List[CubePart]:
        parts = []
        for side, i, j in self.cube.iterate_components():
            x, y, z = self.cube.get_absolute_coordinates(side, i, j)
            y = self.cube.shape[2] - 1 - y
            z = self.cube.shape[1] - 1 - z

            part = self._create_part(x, y, z, self._get_colors(side, i, j))
            parts.append(part)
            self.cube.set_data(Orientation.regular(side), i, j, part)
        return parts

    def _create_part(self, x: int, y: int, z: int, colors: List[Color]) -> CubePart:
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

        vao = self.vao_flat if num_corners == 1 else self.vao_edge if num_corners == 2 else self.vao_corner
        part = CubePart(vao, self.shader, position, axis, colors, self.color_theme)
        return part

    def draw(self, cam_transform: Array, cam_projection: Array) -> None:
        self.shader.use()

        rotation = self.rotation
        if self.temp_rotation != [0, 0, 0]:
            rotation = rotate_x(self.temp_rotation[0]) * \
                       rotate_y(self.temp_rotation[1]) * \
                       rotate_z(self.temp_rotation[2]) * \
                       self.rotation
        glUniformMatrix4fv(self.shader.uniforms["cubeTransform"], 1, GL_TRUE, rotation.to_ctypes())
        glUniformMatrix4fv(self.shader.uniforms["cameraTransform"], 1, GL_TRUE, cam_transform)
        glUniformMatrix4fv(self.shader.uniforms["cameraProjection"], 1, GL_TRUE, cam_projection)

        self.stickers_texture.activate(0)
        glUniform1i(self.shader.uniforms["tex"], 0)
        self.labels_texture.activate(1)
        glUniform1i(self.shader.uniforms["labels_tex"], 1)
        if self.label is not None:
            self.label.texture.activate(2)
            glUniform1i(self.shader.uniforms["label"], 2)
            glUniform1f(self.shader.uniforms["label_scale"], self.label.scale)

        for part in self.parts:
            part.draw()

    def apply_rotation(self):
        self.rotation = (rotate_x(self.temp_rotation[0]) *
                         rotate_y(self.temp_rotation[1]) *
                         rotate_z(self.temp_rotation[2]) *
                         self.rotation)
        self.temp_rotation = [0, 0, 0]
