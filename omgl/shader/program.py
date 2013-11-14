from __future__ import absolute_import
import re
import numpy as np
from OpenGL import GL
from OpenGL.error import Error, GLError
from .shader import Shader


def create(*shaders, **attributes):
    return Program(*shaders, **attributes)

def load(vertex, fragment, **attributes):
    with open(vertex, 'r') as f:
        source = f.read()
        vs = Shader(Shader.vertex, source)
    with open(fragment, 'r') as f:
        source = f.read()
        fs = Shader(Shader.fragment, source)
    return Program(vs, fs, **attributes)


class ProgramException(Exception):
    pass


class Program(object):
    def __init__(self, *shaders, **attributes):
        self._handle = GL.glCreateProgram()

        self.shaders = shaders

        # attach our shaders
        for shader in shaders:
            GL.glAttachShader(self._handle, shader.handle)

        # set attributes
        for name, value in attributes.iteritems():
            GL.glBindAttribLocation(self._handle, value, name)

        self.link()

        # initialise attributes and uniforms
        self.attributes = Attributes(self)
        self.uniforms = Uniforms(self)

    def __del__(self):
        self.delete()

    def delete(self):
        if GL:
            GL.glDeleteShader(self._handle)
            self._handle = None

    def bind(self):
        GL.glUseProgram(self._handle)

    def unbind(self):
        GL.glUseProgram(0)

    def __enter__(self):
        self.bind()

    def __exit__(self, exc_type, exc_value, traceback):
        self.unbind()

    @property
    def handle(self):
        return self._handle

    def link(self):
        GL.glLinkProgram(self._handle)

        if not GL.glGetProgramiv(self._handle, GL.GL_LINK_STATUS):
            errors = GL.glGetProgramInfoLog(self._handle)
            raise ProgramException(errors)

    def sync(self):
        with self:
            self.attributes.sync()
            self.uniforms.sync()


class Variables(object):
    def __init__(self, program, variables):
        self.program = program
        self._variables = variables

    def sync(self):
        for variable in self._variables.itervalues():
            variable.sync()

    def __getitem__(self, key):
        return self._variables[key].get()

    def __setitem__(self, key, value):
        self._variables[key].set(value)


class Attributes(Variables):
    _variable_string_size = 90

    def __init__(self, program):
        variables = {
            name: Attribute(program, name, size, type)
            for name, size, type in self._iter(program)
        }
        Variables.__init__(self, program, variables)

    @classmethod
    def _iter(cls, program):
        count = GL.glGetProgramiv(program.handle, GL.GL_ACTIVE_ATTRIBUTES)
        for index in range(count):
            glNameSize = (GL.constants.GLsizei)()
            glSize = (GL.constants.GLint)()
            glType = (GL.constants.GLenum)()
            glName = (GL.constants.GLchar * cls._variable_string_size)()

            GL.glGetActiveAttrib(program.handle, index, cls._variable_string_size, glNameSize, glSize, glType, glName)

            name, size, type = str(glName.value), glSize.value, glType.value
            yield name, size, type


class Uniforms(Variables):
    def __init__(self, program):
        variables = {
            name: Uniform(program, name, size, type)
            for name, size, type in self._iter(program)
        }
        Variables.__init__(self, program, variables)

    @classmethod
    def _iter(cls, program):
        count = GL.glGetProgramiv(program.handle, GL.GL_ACTIVE_UNIFORMS)
        for index in range(count):
            name, size, type = GL.glGetActiveUniform(program.handle, index)
            yield name, size, type


class Variable(object):
    def __init__(self, program):
        self.program = program
        self._dirty = False
        self._location = None

    @property
    def location(self):
        return self._location



class Attribute(Variable):
    def __init__(self, program, *args):
        Variable.__init__(self, program)
        self.name, self.size, self.type = args
        self._location = int(GL.glGetAttribLocation(self.program.handle, self.name))

    @Variable.location.setter
    def location(self, location):
        self._location = location
        self._dirty = True

    def sync(self):
        if self._dirty:
            GL.glBindAttribLocation(self.program.handle, location, name)
            self._dirty = False

    def get(self):
        return self.location

    def set(self, value):
        self.location = value


class Uniform(Variable):
    re_matrix = re.compile(r'_MAT(?P<size>[\dx]+)')
    re_vector = re.compile(r'_VEC(?P<dimensions>\d)')

    def __init__(self, program, *args):
        Variable.__init__(self, program)
        self.name, _, self.type = args
        self._location = int(GL.glGetUniformLocation(self.program.handle, self.name))
        self._value = None
        self.func, self.size, self.dtype = self._parse_type(self.type)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, (list, tuple)):
            value = np.array(value, dtype=self.dtype)
        self._value = value
        self._dirty = True

    def sync(self):
        if self._dirty:
            if isinstance(self._value, np.ndarray):
                count = self._value.size / self.size
            else:
                count = 1
            self.func(self.location, count, self._value)
            self._dirty = False

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    @classmethod
    def _parse_type(cls, type):
        """Parses the GL enumeration for the uniform and returns the
        appropriate function to use to set uniform data.
        """
        # glUniform{size}{type}v
        #   glUniform2iv
        #   glUniform4uiv
        #   glUniform1fv
        # glUniformMatrix{size}{type}v
        #   glUniformMatrix2fv
        #   glUniformMatrix3x2fv

        dimensions, size, type = 1, 1, 'i'
        
        if '_UNSIGNED_INT' in type:
            type = 'ui'
        elif '_FLOAT' in type:
            type = 'f'

        # special case for matrix
        match = Uniform.re_matrix.search(type)
        if match:
            dimensions = match.group('size')
            dimensions = dimensions.split('x')
            # ensure size is 2 dimensions
            # if not, duplicate the size, ie Mat2 -> [2] -> [2, 2] = 4
            if len(size) == 1:
                size = size * 2
            size = reduce(lambda x, y: x*y, dimensions)

            # matrix functions have a different function name
            dimensions = 'Matrix{dimensions}'.format(dimensions='x'.join(dimensions))

        # vectors
        match = Uniform.re_vector.search(type)
        if match:
            dimensions = match.group('dimensions')
            size = int(dimensions)

        func_string = 'glUniform{dimensions}{type}v'.format(dimensions=dimensions, type=type)
        func = getattr(GL, func_string)
        
        dtype = {
            'i':    np.int32,
            'ui':   np.uint32,
            'f':    np.float32,
        }[type]

        return func, size, dtype
