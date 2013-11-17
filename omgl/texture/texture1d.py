from __future__ import absolute_import
from OpenGL import GL
from .texture import Texture


def create(data, internal_format=None, **kwargs):
    texture = Texture1D(data, internal_format, **kwargs)
    texture.sync()
    return texture

def empty(shape, dtype=None, internal_format=None, **kwargs):
    data = np.empty(shape, dtype=dtype)
    return Texture1D(data, internal_format, **kwargs)   


class Texture1D(Texture):
    def __init__(self, data, internal_format=None, **kwargs):
        Texture.__init__(self, data, GL.GL_TEXTURE_1D, internal_format, **kwargs)
