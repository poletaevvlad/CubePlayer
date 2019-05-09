from OpenGL.GL import *
from ctypes import *
from typing import List, Tuple
from pathlib import Path


nullptr = c_void_p(0)


class VAO:
    def __init__(self):
        self.vao_id = glGenVertexArrays(1)
        self.arrays: List[GLuint] = []
        self.elements_buffer: GLuint = 0
        self.elements_count: int = 0

    def array(self, data: Array, *attribs: Tuple[GLuint, GLint, GLenum, GLboolean, GLsizei, GLsizei]):
        self.bind()
        vbo_id: GLuint = glGenBuffers(1)
        glBindVertexArray(self.vao_id)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
        glBufferData(GL_ARRAY_BUFFER, sizeof(data), data, GL_STATIC_DRAW)

        for index, size, type, normalized, stride, pointer in attribs:
            glEnableVertexAttribArray(index)
            glVertexAttribPointer(index, size, type, normalized, stride, pointer)
        self.arrays.append(vbo_id)

    def elements(self, indices: Array):
        self.bind()
        eab_id: GLuint = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, eab_id)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW)
        self.elements_buffer = eab_id
        self.elements_count = len(indices)

    def bind(self):
        glBindVertexArray(self.vao_id)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.elements_buffer)

    def draw(self):
        self.bind()
        glDrawElements(GL_TRIANGLES, self.elements_count, GL_UNSIGNED_SHORT, nullptr)

    def destroy(self):
        glBindVertexArray(0)
        glDeleteVertexArrays(self.vao_id)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        for array in self.arrays:
            glDeleteBuffers(array)
        glDeleteBuffers(self.elements_buffer)


# noinspection PyCallingNonCallable,PyTypeChecker
def create_quad() -> VAO:
    vertices = (c_float * 8)(-1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0)
    indices = (c_ushort * 6)(1, 0, 2, 2, 0, 3)

    vao = VAO()
    vao.array(vertices, (0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(c_float), c_void_p(0)))
    vao.elements(indices)
    return vao


def obj_parse_face_descriptor(face: str) -> Tuple[int, int, int]:
    face = face.split("/")
    assert len(face) == 3
    return int(face[0]) - 1, int(face[1]) - 1, int(face[2]) - 1


# noinspection PyCallingNonCallable, PyTypeChecker
def load_obj(file: Path) -> VAO:
    vertices: List[Tuple[float, ...]] = []
    normals: List[Tuple[float, ...]] = []
    uvs: List[Tuple[float, ...]] = []
    faces: List[Tuple[Tuple[int, int], ...]] = []

    with open(str(file)) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0 or line[0] in {"#", "o", "g", "s"}:
                continue

            components = list(filter(lambda x: len(x) > 0, map(str.strip, line.split(" "))))
            command = components[0]
            arguments = components[1:]

            if command == "v":
                assert len(arguments) in {3, 4}
                vertices.append(tuple(map(float, arguments))[:3])
            elif command == "vn":
                assert len(arguments) == 3
                normals.append(tuple(map(float, arguments)))
            elif command == "vt":
                assert len(arguments) == 2
                uvs.append(tuple(map(float, arguments)))
            elif command == "f":
                if len(arguments) != 3:
                    raise ValueError("Obj file must be triangulated")
                faces.append(tuple(map(obj_parse_face_descriptor, arguments)))
            else:
                raise ValueError(f"Unknown Obj directive: '{command}'")

    count = len(vertices)
    vert_buffer = (c_float * (count * 3))(*(t for v in vertices for t in v))
    norm_buffer = (c_float * (count * 3))()
    uv_buffer = (c_float * (count * 2))()
    indices = (c_ushort * (len(faces) * 3))()

    for i, ((v1, uv1, n1), (v2, uv2, n2), (v3, uv3, n3)) in enumerate(faces):
        indices[i * 3: i * 3 + 3] = v1, v2, v3
        for v, n, uv in [(v1, n1, uv1), (v2, n2, uv2), (v3, n3, uv3)]:
            norm_buffer[v * 3: v * 3 + 3] = normals[n]
            uv_buffer[v * 2: v * 2 + 2] = uvs[uv]

    vao = VAO()
    vao.array(vert_buffer, (0, 3, GL_FLOAT, GL_FALSE, sizeof(c_float) * 3, c_void_p(0)))
    vao.array(norm_buffer, (1, 3, GL_FLOAT, GL_FALSE, sizeof(c_float) * 3, c_void_p(0)))
    vao.array(uv_buffer, (2, 2, GL_FLOAT, GL_FALSE, sizeof(c_float) * 2, c_void_p(0)))
    vao.elements(indices)
    return vao
