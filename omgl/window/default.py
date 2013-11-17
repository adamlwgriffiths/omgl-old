from __future__ import absolute_import
from .window import WindowException

imported = False
modules = [
    'omgl.window.glfw3_window',
    'omgl.window.freeglut_window',
]

for module in modules:
    try:
        default = __import__(module, fromlist=[""])
        imported = True
        break
    except Exception as e:
        print e



def create(size, title, gl_version=None, gl_forward_compat=True, **kwargs):
    if not imported:
        raise WindowException('No window provider found')

    window = default.create(size, title, gl_version, gl_forward_compat, **kwargs)
    return window
