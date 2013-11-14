import numpy as np
from OpenGL import GL

def primitive_count(type, count):
    def points():
        return count
    def line_strip():
        # the first 2 indices are a line
        # every indice after that is a line
        if count < 2:
            return 0
        return 1 + count - 2
    def line_loop():
        raise NotImplementedError
    def lines():
        return count / 2
    def line_strip_adjacency():
        raise NotImplementedError
    def line_adjacency():
        raise NotImplementedError
    def triangle_strip():
        # the first 3 indices are a triangle
        # every indice after that is a triangle
        if count < 3:
            return 0
        return 1 + count - 3
    def triangle_fan():
        # the first 3 indices are a triangle
        # every indice after that is a triangle
        if count < 3:
            return 0
        return 1 + count - 3
    def triangles():
        return count / 3
    def triangle_strip_adjacency():
        raise NotImplementedError
    def triangle_adjacency():
        raise NotImplementedError
    def patches():
        raise NotImplementedError
    def quads():
        return count / 4
    def quad_strip():
        if count < 4:
            return 0
        return 1 + count - 4
    def polygon():
        # is this just 'count'?
        raise NotImplementedError

    return {
        GL.GL_POINTS:       points,
        GL.GL_LINE_STRIP:   line_strip,
        GL.GL_LINE_LOOP:    line_loop,
        GL.GL_LINES:        lines,
        GL.GL_LINE_STRIP_ADJACENCY: line_strip_adjacency,
        GL.GL_LINES_ADJACENCY:  line_adjacency,
        GL.GL_TRIANGLE_STRIP:   triangle_strip,
        GL.GL_TRIANGLE_FAN: triangle_fan,
        GL.GL_TRIANGLES:    triangles,
        GL.GL_TRIANGLE_STRIP_ADJACENCY: triangle_strip_adjacency,
        GL.GL_TRIANGLES_ADJACENCY:  triangle_adjacency,
        GL.GL_PATCHES:      patches,
        GL.GL_QUADS:        quads,
        GL.GL_QUAD_STRIP:   quad_strip,
        GL.GL_POLYGON:      polygon,
    }[type]()

def np_type_to_gl_enum(type):
    return {
        np.uint8:       GL.GL_UNSIGNED_BYTE,
        np.uint16:      GL.GL_UNSIGNED_SHORT,
        np.uint32:      GL.GL_UNSIGNED_INT,
        np.int8:        GL.GL_BYTE,
        np.int16:       GL.GL_SHORT,
        np.int32:       GL.GL_INT,
        np.float32:     GL.GL_FLOAT,
        np.float64:     GL.GL_DOUBLE,
        # http://docs.python.org/2/library/platform.html#cross-platform
        # probably best to explode if user's aren't explicit about the size
        #np.float:       GL.GL_DOUBLE if sys.maxsize > 2**32 else GL.GL_FLOAT,
    }[type]

def memoize(obj):
    """Decorator to cache the output of functions.
    """
    cache = obj.cache = {}

    import functools
    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer
