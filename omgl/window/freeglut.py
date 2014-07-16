from __future__ import absolute_import
import sys
import atexit
from .window import Window, WindowException

try:
    from OpenGL import GLUT
    from OpenGL.GLUT import freeglut

    def initialise():
        if not FreeGLUT_Window.initialised:
            GLUT.glutInit(sys.argv)
            freeglut.glutSetOption(freeglut.GLUT_ACTION_ON_WINDOW_CLOSE, freeglut.GLUT_ACTION_CONTINUE_EXECUTION)
            FreeGLUT_Window.initialised = True

    def create(size, title, gl_version=None, gl_forward_compat=True, **kwargs):
        return FreeGLUT_Window(size, title, gl_version, gl_forward_compat, **kwargs)


    class FreeGLUT_Window(Window):
        initialised = False
        def __init__(self, size, title, gl_version=None, gl_forward_compat=True, **kwargs):
            initialise()

            self._title = title

            GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGBA | GLUT.GLUT_DEPTH)
            GLUT.glutInitWindowSize(size[0], size[1])
            self.handle = GLUT.glutCreateWindow(title)

            self.activate()

            GLUT.glutKeyboardFunc(self.on_key_press)
            GLUT.glutSpecialFunc(self.on_special_press)

        @property
        def title(self):
            return self._title

        @title.setter
        def title(self, title):
            current = GLUT.glutGetWindow()
            self.activate()
            self._title = title
            GLUT.glutSetWindowTitle(title)
            GLUT.glutSetWindow(current)

        def activate(self):
            GLUT.glutSetWindow(self.handle)

        def poll_events(self):
            freeglut.glutMainLoopEvent()

        def swap_buffers(self):
            GLUT.glutSwapBuffers()

        def close(self):
            if self.handle:
                # A bug in GLUT makes the last destroyed window not disappear
                # this happens on OS-X at least
                GLUT.glutHideWindow(self.handle)
                GLUT.glutDestroyWindow(self.handle)
                self.handle = None

        def on_key_press(self, key, x, y):
            # get the modifiers
            mods = GLUT.glutGetModifiers()

        def on_special_press(self, key, x, y):
            # get the modifiers
            mods = GLUT.glutGetModifiers()

except:
    pass
