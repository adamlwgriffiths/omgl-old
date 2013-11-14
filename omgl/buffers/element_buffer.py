from __future__ import absolute_import
import numpy as np
from OpenGL import GL
from .buffer import Buffer
from ..utilities import np_type_to_gl_enum


def empty(shape, dtype, polygons=None, usage=GL.GL_DYNAMIC_DRAW):
    data = np.empty(shape, dtype=dtype)
    return ElementBuffer(data, polygons, usage)

def npdata(data, polygons=None, usage=GL.GL_DYNAMIC_DRAW):
    buffer = ElementBuffer(data, polygons, usage)
    buffer.sync()
    return buffer


class ElementBuffer(Buffer):
    def __init__(self, data, polygons=None, usage=GL.GL_DYNAMIC_DRAW):
        Buffer.__init__(self, GL.GL_ELEMENT_ARRAY_BUFFER, data, usage)
        self.polygons = polygons or {}

    def draw(self, name=None, polygon_type=None):
        def draw_(name, polygon_type):
            count = reduce(lambda x, y: x*y, self._data.dtype[name].subdtype[1])
            dtype = np_type_to_gl_enum(self._data.dtype[name].subdtype[0].type)
            offset = self._data.dtype.fields[name][1]

            GL.glDrawElements(polygon_type, count, dtype, offset)

        if name:
            draw_(name, polygon_type)
        else:
            if len(self.polygons):
                for name, polygon_type in self.polygons.iteritems():
                    draw_(name, polygon_type)
            else:
                # polygon_type = ???
                # count = self._data.size
                # dtype = dtype
                # offset = 0
                #GL.glDrawElements()
                raise NotImplementedError
