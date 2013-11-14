from __future__ import absolute_import
import numpy as np
from OpenGL import GL


def empty(target, shape, dtype=None, usage=GL.GL_DYNAMIC_DRAW):
    # we assume float32 for opengl
    if not dtype:
        dtype = np.float32
        
    data = np.empty(shape, dtype=dtype)
    return Buffer(target, data, usage)

def npdata(target, data, usage=GL.GL_DYNAMIC_DRAW):
    buffer = Buffer(target, data, usage)
    buffer.sync()
    return buffer


class Buffer(object):
    """An OpenGL Vertex Buffer Object (VBO) wrapper.
    """
    def __init__(self, target, data, usage):
        self._handle = GL.glGenBuffers(1)
        self._target = target
        self._usage = usage
        self._data = data

        self._create()

    def __del__(self):
        self.delete()

    def delete(self):
        """Deletes the OpenGL object.
        """
        if GL:
            GL.glDeleteBuffers(1, [self._handle])
            self._handle = None

    def _create(self):
        with self:
            GL.glBufferData(self._target, self._data.nbytes, None, self._usage)

    def bind(self):
        """Sets this object as the active buffer for this target.
        """
        GL.glBindBuffer(self._target, self._handle)

    def unbind(self):
        """Sets the active buffer for this target to 0.
        """
        GL.glBindBuffer(self._target, 0)

    def __enter__(self):
        """Calls bind().
        """
        self.bind()

    def __exit__(self, exc_type, exc_value, traceback):
        """Calls unbind().
        """
        self.unbind()

    @property
    def data(self):
        """The cached data.
        """
        return self._data

    @data.setter
    def data(self, data):
        """Used to change the 
        """
        if not isinstance(data, np.ndarray):
            data = np.array(data)

        # check if the size changed
        original_nbytes = self._data.nbytes
        self._data = data

        if self._data.nbytes != original_nbytes:
            self._create()

    @property
    def handle(self):
        return self._handle

    @property
    def target(self):
        return self._target

    @property
    def usage(self):
        return self._usage

    def sync(self):
        """Flushes the cached data to OpenGL.
        """
        with self:
            GL.glBufferSubData(self._target, 0, self._data.nbytes, self._data)

    def get_data(self):
        """Returns the data stored in OpenGL.

        This function should only be used for debugging as it is slow.
        Use the cached data in the data property.
        """
        gl_data = np.empty_like(self._data)
        with self:
            GL.glGetBufferSubData(self._target, 0, gl_data.nbytes, gl_data)
        return gl_data
