from gi.repository import Gtk

from .visualizer import CubeVisualizer
from libcube.actions import Action
from typing import List


class MainWindow(Gtk.Window):
    def __init__(self, formula: List[Action]):
        super().__init__()
        self.set_size_request(800, 600)

        view = CubeVisualizer()
        view.set_formula(formula)
        self.add(view)
        view.show()
