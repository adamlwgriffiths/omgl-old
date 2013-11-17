
class WindowException(Exception):
    pass

class Window(object):
    def __init__(self, size, title, gl_version=None, gl_forward_compat=True, **kwargs):
        pass

    def __del__(self):
        self.close()

    def run(self, main_loop):
        while True:
            self.poll_events()
            if not main_loop():
                return
            self.swap_buffers()

    def activate(self):
        pass

    def poll_events(self):
        pass

    def swap_buffers(self):
        pass

    def close(self):
        pass


from . import default

