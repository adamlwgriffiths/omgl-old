from __future__ import absolute_import
import numpy as np
from OpenGL import GL
from OpenGL.GL.ARB import texture_rg
from schematics.models import Model, ModelMeta
from schematics.types import BaseType
from collections import OrderedDict
from ..utilities import np_type_to_gl_enum


# TODO: add glCopyTexSubImage - allows you to overlay texture data onto another texture
# TODO: add mipmap generation support, dont bother with manual mipmap uploading


def create(data, target=None, internal_format=None, **kwargs):
    texture = Texture(data, target, internal_format, **kwargs)
    texture.sync()
    return texture

def empty(shape, dtype=None, target=None, internal_format=None, **kwargs):
    data = np.empty(shape, dtype=dtype)
    return Texture(data, target, internal_format, **kwargs)   

def load(filename):
    pass


class TexturePropertyType(BaseType):
    def __init__(self, enum, **kwargs):
        BaseType.__init__(self, **kwargs)
        self.enum = enum
        self.mode = kwargs.get('default', None)

    def sync(self, texture, mode):
        if self.mode != mode:
            GL.glTexParameteri(texture.target, self.enum, mode)
            self.mode = mode


class TextureMeta(ModelMeta):
    def __new__(cls, name, bases, attrs):
        texture_properties = OrderedDict()

        for base in reversed(bases):
            if hasattr(base, '_texture_properties'):
                texture_properties.update(base._texture_properties)

        for key, value in attrs.items():
            if isinstance(value, TexturePropertyType):
                texture_properties[key] = value

        attrs['_texture_properties'] = texture_properties

        return ModelMeta.__new__(cls, name, bases, attrs)


class Texture(Model):
    __metaclass__ = TextureMeta

    _allocators = {
        1:      GL.glTexImage1D,
        2:      GL.glTexImage2D,
        3:      GL.glTexImage3D,
    }
    _sub_allocators = {
        1:      GL.glTexSubImage1D,
        2:      GL.glTexSubImage2D,
        3:      GL.glTexSubImage3D,
    }

    min_filter = TexturePropertyType(GL.GL_TEXTURE_MIN_FILTER, default=GL.GL_NEAREST_MIPMAP_LINEAR)
    mag_filter = TexturePropertyType(GL.GL_TEXTURE_MAG_FILTER, default=GL.GL_LINEAR)

    def __init__(self, data, target=None, internal_format=None, **kwargs):
        Model.__init__(self, kwargs)

        if not isinstance(data, np.ndarray):
            data = np.array(data)

        self._handle = GL.glGenTextures(1)
        self._target = target or self.infer_target(data)
        self._internal_format = internal_format or self.infer_internal_format(data)
        # schematics uses _data, we must use a different name
        self._npdata = data

        # FIXME: set to linear for non-mipmapped textures
        if 'min_filter' not in kwargs:
            self.min_filter = GL.GL_LINEAR

        self._create()

    def _create(self):
        with self:
            for name, property in self._texture_properties.iteritems():
                value = self._data[name]
                property.sync(self, value)

            format = self.infer_format(self._npdata)

            func = self._allocators[self._npdata.ndim-1]
            args = [self.target, 0, self.internal_format,]
            args += list(self.size)
            args += [0, format, self.type, None]
            func(*args)

    def sync(self):
        with self:
            for name, property in self._texture_properties.iteritems():
                value = self[name]
                property.sync(self, value)

            format = self.infer_format(self._npdata)

            func = self._sub_allocators[self._npdata.ndim-1]
            args = [self.target, 0,]
            args += [0] * (self._npdata.ndim-1)
            args += list(self.size)
            args += [format, self.type, self._npdata]
            func(*args)

    def bind(self, unit):
        GL.glEnable(self.target)
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        GL.glBindTexture(self.target, self.handle)

    def unbind(self, unit):
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        GL.glBindTexture(self.target, 0)
        GL.glDisable(self.target)

    def __enter__(self):
        self.bind(0)

    def __exit__(self, exc_type, exc_value, traceback):
        self.unbind(0)

    def delete(self):
        if GL:
            GL.glDeleteTextures(self.handle)
            self.handle = None

    @property
    def handle(self):
        return self._handle

    @property
    def target(self):
        return self._target

    @property
    def type(self):
        return np_type_to_gl_enum(self._npdata.dtype.type)

    @property
    def internal_format(self):
        return self._internal_format

    @property
    def size(self):
        return self._npdata.shape[:-1]

    @property
    def data(self):
        return self._npdata

    def get_data(self):
        """Returns the data stored in OpenGL.

        This function should only be used for debugging, or sparingly, as it is slow.
        Use the cached 'data' property instead.
        """
        with self:
            # BUG: PyOpenGL doesn't support GL_RG or GL_RG_INTEGER here
            # we have to get the red and green components individually
            #gl_data = GL.glGetTexImage(self._target, 0, self.infer_format(self._npdata), self.type, np.ndarray)
            format = self.infer_format(self._npdata)
            if format == texture_rg.GL_RG_INTEGER or format == texture_rg.GL_RG:
                red_enum = GL.GL_RED_INTEGER if format == texture_rg.GL_RG_INTEGER else GL.GL_RED
                green_enum = GL.GL_GREEN_INTEGER if format == texture_rg.GL_RG_INTEGER else GL.GL_GREEN

                red = GL.glGetTexImage(self._target, 0, red_enum, self.type, np.ndarray)
                green = GL.glGetTexImage(self._target, 0, green_enum, self.type, np.ndarray)
                gl_data = np.empty_like(self._npdata)
                gl_data[...,0] = red
                gl_data[...,1] = green
            else:
                gl_data = GL.glGetTexImage(self._target, 0, format, self.type, np.ndarray)
        gl_data.shape = self._npdata.shape
        return gl_data

    @classmethod
    def infer_target(cls, data):
        try:
            # TODO: add more
            # remove the colour channels from the dimensions
            return {
                1:  GL.GL_TEXTURE_1D,
                2:  GL.GL_TEXTURE_2D,
                3:  GL.GL_TEXTURE_3D,
            }[data.ndim-1]
        except KeyError as e:
            raise ValueError(e.message)

    @classmethod
    def infer_internal_format(cls, data):
        # GL_RED doesn't give us specific types in PyOpenGL, so use GL_R
        # GL_R and GL_RG should be taken from the rg extension
        base, module = {
            1:  ('GL_R', texture_rg),
            2:  ('GL_RG', texture_rg),
            3:  ('GL_RGB', GL),
            4:  ('GL_RGBA', GL),
        }[data.shape[-1]]

        type = {
            np.uint8:   '8UI',
            np.uint16:  '16UI',
            np.uint32:  '32UI',
            np.int8:    '8I',
            np.int16:   '16I',
            np.int32:   '32I',
            np.float16: '16F',
            np.float32: '32F',
        }[data.dtype.type]

        string = base + type
        enum = getattr(module, string)
        return enum

    @classmethod
    def infer_format(cls, data):
        # GL_R and GL_RG should be taken from the rg extension
        base, module = {
            1:  ('GL_RED', GL,),
            2:  ('GL_RG', texture_rg,),
            3:  ('GL_RGB', GL,),
            4:  ('GL_RGBA', GL,),
        }[data.shape[-1]]

        # integral types MUST be post-fixed with _INTEGER
        # https://www.opengl.org/wiki/Pixel_Transfer#Pixel_format
        if not np.issubdtype(data.dtype, float):
            base += '_INTEGER'

        string = base
        enum = getattr(module, string)
        return enum


