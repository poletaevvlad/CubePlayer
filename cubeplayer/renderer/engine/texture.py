from typing import Union

from OpenGL.GL import *
from PIL import Image

from pathlib import Path


class Texture:
    def __init__(self, img: Union[Path, Image.Image], format: GLint = GL_RGB, flip: bool = False,
                 filter: GLint = GL_LINEAR, mipmap: bool = False):
        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id)

        if isinstance(img, Path):
            img = Image.open(str(img))

        if format == GL_RGB:
            img = img.convert("RGB")
            int_format = GL_RGB8
        elif format == GL_RGBA:
            img = img.convert("RGBA")
            int_format = GL_RGBA8
        else:
            raise ValueError("Unsupported base image format")

        if flip:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
        if not mipmap:
            glTexImage2D(GL_TEXTURE_2D, 0, format, *img.size, 0, format, GL_UNSIGNED_BYTE, img.tobytes())
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filter)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filter)
        else:
            glTexStorage2D(GL_TEXTURE_2D, 4, int_format, *img.size)
            glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, *img.size, format, GL_UNSIGNED_BYTE, img.tobytes())
            glGenerateMipmap(GL_TEXTURE_2D)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filter)
            mag_filter = GL_LINEAR_MIPMAP_NEAREST if filter == GL_LINEAR else GL_NEAREST_MIPMAP_NEAREST
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, mag_filter)

    @staticmethod
    def load(filename: str, *args, **kwargs):
        path = Path(__file__).parents[3] / "textures" / (filename + ".png")
        return Texture(path, *args, **kwargs)

    def activate(self, index: int) -> None:
        glActiveTexture(GL_TEXTURE0 + index)
        glBindTexture(GL_TEXTURE_2D, self.id)

    def destroy(self) -> None:
        glDeleteTextures(self.id)
