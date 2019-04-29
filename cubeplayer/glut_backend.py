from OpenGL.GLUT import *
from cubeplayer.renderer.scene import Scene


class GlutWindow:
    def __init__(self):
        self.is_rotating: bool = False
        self.mouse_x: int = 0
        self.mouse_y: int = 0

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_3_2_CORE_PROFILE)
        glutInitContextVersion(3, 3)
        glutInitContextProfile(GLUT_CORE_PROFILE)
        glutInitWindowSize(640, 480)
        glutCreateWindow("CubePlayer")

        self.scene = Scene()
        glutDisplayFunc(self._display)
        glutMouseFunc(self._mouse_handler)
        glutMotionFunc(self._mouse_motion)

    @staticmethod
    def run():
        glutMainLoop()

    def _display(self):
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

