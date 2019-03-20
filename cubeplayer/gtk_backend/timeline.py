from gi.repository import Gtk
import cairo
from abc import ABC, abstractmethod


class ITimelineData(ABC):
    @abstractmethod
    def get_text(self, index: int) -> str:
        pass

    @abstractmethod
    def count(self) -> int:
        pass


class Timeline(Gtk.DrawingArea):
    def __init__(self, data: ITimelineData):
        super(Timeline, self).__init__()
        self.set_size_request(0, 20)
        self.connect("draw", self.on_draw)

        self.current_position = 0.0
        self.slot_width = 30
        self.data: ITimelineData = data

    def on_draw(self, _self, ctx: cairo.Context):
        context: Gtk.StyleContext = self.get_style_context()
        width: int = self.get_allocated_width()
        height: int = self.get_allocated_height()

        background = context.get_background_color(Gtk.StateFlags.BACKDROP)
        ctx.set_source_rgba(*background)
        ctx.rectangle(0, 0, width, height)
        ctx.fill()

        offset = width / 2 - self.current_position * self.slot_width
        min_index = -offset / self.slot_width
        max_index = int(min(min_index + width / self.slot_width + 1, self.data.count()))
        min_index = int(max(min_index, 0))

        border = context.get_color(Gtk.StateFlags.BACKDROP)
        ctx.set_source_rgba(*border)
        ctx.set_line_width(1)
        for index in range(min_index, max_index + 1):
            x = int(offset + self.slot_width * index)
            ctx.move_to(x + 0.5, 10)
            ctx.line_to(x + 0.5, height)

            if index < max_index:
                text = self.data.get_text(index)
                text_extents: cairo.TextExtents = ctx.text_extents(text)
                ctx.move_to(x + self.slot_width / 2 - text_extents.width / 2, 12)
                ctx.show_text(text)
        ctx.stroke()

        marker_color = context.get_color(Gtk.StateFlags.LINK)
        ctx.set_source_rgba(*marker_color)
        ctx.move_to(width / 2 - 3, 0)
        ctx.line_to(width / 2 + 3, 0)
        ctx.line_to(width / 2, 6)
        ctx.fill()
