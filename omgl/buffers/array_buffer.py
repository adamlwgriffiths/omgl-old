from __future__ import absolute_import
import numpy as np
from OpenGL import GL
from .buffer import Buffer


def empty(shape, dtype=None, usage=GL.GL_DYNAMIC_DRAW):
    # we assume float32 for opengl
    if not dtype:
        dtype = np.float32

    data = np.empty(shape, dtype=dtype)
    return Buffer(GL.GL_ARRAY_BUFFER, data, usage)

def npdata(data, usage=GL.GL_DYNAMIC_DRAW):
    buffer = Buffer(GL.GL_ARRAY_BUFFER, data, usage)
    buffer.sync()
    return buffer
