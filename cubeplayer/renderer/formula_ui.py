from OpenGL.GL import *
from pathlib import Path
from typing import Sequence
from .engine.text import FontFace
from .engine.texture import Texture
from .engine.sprite import Sprite


class FormulaUI:
    def __init__(self, items: Sequence[str], scale: float):
        self.items = items
        self.position: float = 0
        self.item_width: int = int(45 * scale)
        self.scale = scale

        path = Path(__file__).parents[2] / "fonts" / "PT_Sans-Regular.ttf"
        self.font = FontFace(path, 16 * scale)
        self.indicator = Sprite(int(16 * scale), int(16 * scale),
                                Texture.load("ui_indicator", GL_RGBA))
        self.separator = Sprite(int(16 * scale), int(16 * scale),
                                Texture.load("ui_separator", GL_RGBA, filter=GL_NEAREST))

    def render(self, width: int, height: int):
        leftmost = round(width / 2 - self.position * self.item_width)
        if leftmost > 0:
            index = 0
        else:
            index = -leftmost // self.item_width

        position = leftmost + self.item_width * index
        while position < width and index < len(self.items):
            self.separator.draw(width, height,
                                position - self.separator.width // 2,
                                height - self.separator.height - int(10 * self.scale))

            self.font.draw(width, height, position + self.item_width // 2,
                           height - int(13 * self.scale), self.items[index], align=0.5)

            index += 1
            position += self.item_width

        self.separator.draw(width, height,
                            position - self.separator.width // 2,
                            height - self.separator.height - 10 * self.scale)
        self.indicator.draw(width, height, (width - self.indicator.width) // 2,
                            height - self.indicator.height)
