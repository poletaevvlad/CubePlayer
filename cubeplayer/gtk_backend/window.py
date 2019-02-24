from gi.repository import Gtk

from .visualizer import CubeVisualizer


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, application):
        super().__init__(application=application)
        self.set_size_request(800, 600)

        view = CubeVisualizer()
        self.add(view)
        view.show()
