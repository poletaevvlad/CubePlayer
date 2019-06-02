import time

from OpenGL.GLUT import *

from .backend import RenderingBackend


class GlutWindow(RenderingBackend):
    def __init__(self, *argv):
        super().__init__(*argv)

        self.is_rotating: bool = False
        self.mouse_x: int = 0
        self.mouse_y: int = 0
        self.time: float = None

    def init_gl(self):
        self.create_glut_window("CubePlayer", True)

        glutDisplayFunc(self._display)
        glutMouseFunc(self._mouse_handler)
        glutMotionFunc(self._mouse_motion)

    def _display(self):
        now = time.clock()
        if self.time is not None:
            self.animator.run(now - self.time)
        self.time = now

        width = glutGet(GLUT_WINDOW_WIDTH)
        height = glutGet(GLUT_WINDOW_HEIGHT)
        self.scene.render(width, height)
        glutSwapBuffers()
        glutPostRedisplay()

    def _mouse_handler(self, button: int, state: int, x: int, y: int):
        if button == GLUT_LEFT_BUTTON:
            self.is_rotating = state == GLUT_DOWN
            self.mouse_x = x
            self.mouse_y = y

    def _mouse_motion(self, x: int, y: int):
        if self.is_rotating:
            self.scene.rotate(x - self.mouse_x, y - self.mouse_y)
            self.mouse_x = x
            self.mouse_y = y

    def run(self):
        glutMainLoop()
