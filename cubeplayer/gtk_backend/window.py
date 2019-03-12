from gi.repository import Gtk

from .visualizer import CubeVisualizer
from libcube.actions import Action
from typing import List
from pathlib import Path
from .timeline import Timeline, ITimelineData


class TimelineData(ITimelineData):
    def get_text(self, index: int) -> str:
        return str(index)

    def count(self) -> int:
        return 10


class MainWindow(Gtk.Window):
    def __init__(self, formula: List[Action]):
        super().__init__()

        header_ui = Path(__file__).parents[2] / "ui" / "header.glade"
        ui_builder = Gtk.Builder()
        ui_builder.add_from_file(str(header_ui))
        header_bar: Gtk.HeaderBar = ui_builder.get_object("header_bar")
        self.set_titlebar(header_bar)

        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        timeline = Timeline(TimelineData())
        timeline.show()
        container.pack_start(timeline, False, False, 0)

        view = CubeVisualizer()
        view.show()
        container.pack_end(view, True, True, 0)

        self.add(container)
        container.show()

