from __future__ import absolute_import
from schematics.types import BaseType
from omgl.gl import glsl_version


# TODO: handle uniform array types
# varying vec3 texture_coords[];

class ShaderType(BaseType):
    def source(self):
        raise NotImplementedError

class ShaderMacroType(ShaderType):
    pass

class ExtensionType(ShaderMacroType):
    enable = 'enable'
    require = 'require'
    warn = 'warn'
    disable = 'disable'

    def __init__(self, extension, mode=None, enable=None, require=None, warn=None, disable=None, **kwargs):
        super(ExtensionType, self).__init__(**kwargs)
        self.extension = extension
        if mode:
            self.mode = mode
        elif enable:
            self.mode = self.enable
        elif require:
            self.mode = self.require
        elif warn:
            self.mode = self.warn
        elif disable:
            self.mode = self.disable

    def source(self):
        return '#extension {extension} : {mode}'.format(
            extension=self.extension,
            mode=self.mode
        )

class RawTextType(ShaderMacroType):
    def __init__(self, text, **kwargs):
        super(RawTextType, self).__init__(**kwargs)
        self.text = text

    def source(self):
        return self.text

class ShaderVariableType(ShaderType):
    def __init__(self, type, **kwargs):
        super(ShaderVariableType, self).__init__(**kwargs)
        self.type = type

class UniformType(ShaderVariableType):
    def source(self, name):
        return 'uniform {type} {name};'.format(type=self.type, name=name)

class UniformArrayType(ShaderVariableType):
    def __init__(self, type, count=None, **kwargs):
        super(UniformArrayType, self).__init__(type, **kwargs)
        self.count = count

    def source(self, name):
        count = self.count or ''
        return 'uniform {type} {name}[{count}];'.format(type=self.type, name=name, count=count)

class AttributeType(ShaderVariableType):
    def source(self, name):
        if glsl_version() <= 120:
            string = 'attribute {type} {name};'
        else:
            string = 'in {type} {name};'
        return string.format(type=self.type, name=name)

class VaryingType(ShaderVariableType):
    input = 'in'
    output = 'out'

    def __init__(self, type, direction=None, input=None, output=None, **kwargs):
        super(VaryingType, self).__init__(type, **kwargs)
        if direction:
            self.direction = direction
        elif input is not None:
            self.direction = self.input if input else self.output
        elif output is not None:
            self.direction = self.output if output else self.input

    def source(self, name):
        if glsl_version() <= 120:
            string = 'varying {type} {name};'
        else:
            string = '{direction} {type} {name};'
        return string.format(direction=self.direction, type=self.type, name=name)

class FragType(ShaderVariableType):
    def __init__(self, type, **kwargs):
        super(FragType, self).__init__(type, **kwargs)

    def source(self, name):
        if glsl_version() <= 120:
            return ''

        string = '{direction} {type} {name};'
        return string.format(direction='out', type=self.type, name=name)

