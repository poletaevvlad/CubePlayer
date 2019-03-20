from pathlib import Path
from typing import List, Tuple

from gi.repository import GLib
from gi.repository import Gdk
from gi.repository import Gtk

from libcube.actions import Action
from libcube.parser import get_action_representation
from renderer import Scene
from renderer.animation import Animator
from renderer.cube_animation import CubeAnimationManager
from .timeline import Timeline, ITimelineData
from .visualizer import CubeVisualizer


class TimelineData(ITimelineData):
    def __init__(self, formula: List[Action]):
        self.formula: List[str] = list(map(get_action_representation, formula))

    def get_text(self, index: int) -> str:
        return self.formula[index]

    def count(self) -> int:
        return len(self.formula)


class MainWindow(Gtk.Window):
    def __init__(self, formula: List[Action]):
        super().__init__()
        self.timeline, self.visualizer = self._init_ui(TimelineData(formula))
        self.scene = None
        self.animator = None
        self.cube_animator = None
        self.prev_animation_time = None

    def _init_ui(self, data: TimelineData) -> Tuple[Timeline, CubeVisualizer]:
        header_ui = Path(__file__).parents[2] / "ui" / "header.glade"
        ui_builder = Gtk.Builder()
        ui_builder.add_from_file(str(header_ui))
        header_bar: Gtk.HeaderBar = ui_builder.get_object("header_bar")
        self.set_titlebar(header_bar)

        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        timeline = Timeline(data)
        timeline.show()
        container.pack_start(timeline, False, False, 0)

        view = CubeVisualizer(self._init_callback)
        view.show()
        container.pack_end(view, True, True, 0)

        self.add(container)
        container.show()
        return timeline, view

    def _init_callback(self, scene: Scene) -> None:
        self.scene = scene
        self.animator = Animator()
        self.cube_animator = CubeAnimationManager(self.scene.cube, self.animator, self.scene.camera)
        self.add_tick_callback(self._on_tick)

    def _on_tick(self, _self: Gtk.Window, frame_clock: Gdk.FrameClock) -> bool:
        frame_time = frame_clock.get_frame_time()
        if self.prev_animation_time is not None:
            delta_time = (frame_time - self.prev_animation_time) / 1000
            self.animator.run(delta_time)
            self.visualizer.queue_render()

        self.prev_animation_time = frame_time
        return GLib.SOURCE_CONTINUE
