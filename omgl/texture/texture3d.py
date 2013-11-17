from __future__ import absolute_import
from OpenGL import GL
from .texture import Texture
from .types import TexturePropertyType


def create(data, internal_format=None, **kwargs):
    texture = Texture3D(data, internal_format, **kwargs)
    texture.sync()
    return texture

def empty(shape, dtype=None, internal_format=None, **kwargs):
    data = np.empty(shape, dtype=dtype)
    return Texture3D(data, internal_format, **kwargs)   


class Texture3D(Texture):
    wrap_s = TexturePropertyType(GL.GL_TEXTURE_WRAP_S, default=GL.GL_REPEAT)
    wrap_t = TexturePropertyType(GL.GL_TEXTURE_WRAP_T, default=GL.GL_REPEAT)
    wrap_r = TexturePropertyType(GL.GL_TEXTURE_WRAP_R, default=GL.GL_REPEAT)

    def __init__(self, data, internal_format=None, **kwargs):
        Texture.__init__(self, data, GL.GL_TEXTURE_3D, internal_format, **kwargs)
