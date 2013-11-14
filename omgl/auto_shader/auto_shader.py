from __future__ import absolute_import
from schematics.models import Model, ModelMeta
from schematics.types import BaseType
from collections import OrderedDict
from omgl.shader.shader import Shader
from .types import ShaderMacroType, ShaderVariableType

# provide hierarchical access
from .decorators import glsl
from .types import (
    ExtensionType, RawTextType,
    ShaderVariableType, UniformType, UniformArrayType, AttributeType, VaryingType, FragType
)


class ShaderMeta(ModelMeta):
    def __new__(cls, name, bases, attrs):
        glsl_macros = OrderedDict()
        glsl_variables = OrderedDict()
        glsl_decorators = OrderedDict()

        for base in reversed(bases):
            if hasattr(base, '_glsl_macros'):
                glsl_macros.update(base._glsl_macros)
            if hasattr(base, '_glsl_variables'):
                glsl_variables.update(base._glsl_variables)
            if hasattr(base, '_glsl_decorators'):
                glsl_decorators.update(base._glsl_decorators)

        for key, value in attrs.items():
            if isinstance(value, ShaderVariableType):
                glsl_variables[key] = value
            elif isinstance(value, ShaderMacroType):
                glsl_macros[key] = value
            elif hasattr(value, '_glsl_decorator'):
                glsl_decorators[key] = value._glsl_decorator

        attrs['_glsl_macros'] = glsl_macros
        attrs['_glsl_variables'] = glsl_variables
        attrs['_glsl_decorators'] = glsl_decorators

        return ModelMeta.__new__(cls, name, bases, attrs)

class AutoShader(Shader, Model):
    __metaclass__ = ShaderMeta

    def __init__(self, type, **kwargs):
        Model.__init__(self, raw_data=kwargs)
        Shader.__init__(self, type, self._gather_source())

    def _gather_source(self):
        # process our defines
        macros = [
            macro.source()
            for name, macro in self._glsl_macros.iteritems()
        ]

        # process the variables first
        variables = [
            variable.source(name)
            for name, variable in self._glsl_variables.iteritems()
        ]

        # pre-declare all functions
        predeclarations = [
            function.signature() + ';'
            for name, function in self._glsl_decorators.iteritems()
        ]

        # process the function source
        functions = [
            function.source(self)
            for name, function in self._glsl_decorators.iteritems()
        ]

        # convert to a source string
        source = '\n'.join(
            macros + [''] + variables + [''] + predeclarations + [''] + functions
        )
        return source


class FragmentAutoShader(AutoShader):
    def __init__(self, **kwargs):
        super(FragmentAutoShader, self).__init__(AutoShader.fragment, **kwargs)

class VertexAutoShader(AutoShader):
    def __init__(self, **kwargs):
        super(VertexAutoShader, self).__init__(AutoShader.vertex, **kwargs)

