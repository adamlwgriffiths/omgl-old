from OpenGL import GL
from schematics.types import BaseType

class TexturePropertyType(BaseType):
    def __init__(self, enum, **kwargs):
        BaseType.__init__(self, **kwargs)
        self.enum = enum
        self.mode = kwargs.get('default', None)

    def sync(self, texture, mode):
        if self.mode != mode:
            GL.glTexParameteri(texture.target, self.enum, mode)
            self.mode = mode
