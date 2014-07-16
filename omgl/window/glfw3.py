from __future__ import absolute_import
import atexit
import cyglfw3 as glfw
from .window import Window, WindowException

try:
    import cyglfw3 as glfw

    def initialise():
        if not GLFW_Window.initialised:
            if not glfw.Init():
                raise WindowException('Failed to initialise GLFW')

            glfw.SetErrorCallback(error_callback)

            GLFW_Window.initialised = True

    @atexit.register
    def shutdown():
        if GLFW_Window.initialised:
            glfw.Terminate()
            GLFW_Window.initialised = False

    last_error = None
    def error_callback(error, message):
        global last_error
        last_error = message

    def create(size, title, gl_version=None, gl_forward_compat=True, **kwargs):
        return GLFW_Window(size, title, gl_version, gl_forward_compat, **kwargs)


    class GLFW_Window(Window):
        initialised = False
        def __init__(self, size, title, gl_version=None, gl_forward_compat=True, **kwargs):
            initialise()

            self._title = title

            if gl_version:
                glfw.WindowHint(glfw.CONTEXT_VERSION_MAJOR, gl_version[0])
                glfw.WindowHint(glfw.CONTEXT_VERSION_MINOR, gl_version[1])
                if gl_version[0] >= 3:
                    glfw.WindowHint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
                    if gl_forward_compat:
                        glfw.WindowHint(glfw.OPENGL_FORWARD_COMPAT, gl_forward_compat)

            self.handle = glfw.CreateWindow(size[0], size[1], title)

            if not self.handle:
                raise WindowException(self.last_error)

            self.activate()

        @property
        def title(self):
            return self._title

        @title.setter
        def title(self, title):
            self._title = title
            return glfw.SetWindowTitle(self.handle, title)

        def activate(self):
            glfw.MakeContextCurrent(self.handle)

        def poll_events(self):
            glfw.PollEvents()

        def swap_buffers(self):
            glfw.SwapBuffers(self.handle)

        def close(self):
            if self.handle:
                glfw.DestroyWindow(self.handle)
                self.handle = None
except:
    pass
