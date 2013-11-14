from __future__ import absolute_import
import re
import textwrap
from OpenGL import GL
from OpenGL.error import Error, GLError


def create(type, source):
    return Shader(type, source)

def load(type, filename):
    with open(filename, 'r') as f:
        source = f.read()
        return Shader(type, source)


class ShaderException(Exception):
    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return '\n'.join(map(str, self.errors))


class ShaderError(object):
    def __init__(self, cls, type, description, line, source):
        self.cls = cls
        self.type = type
        self.description = description
        self.line = line
        self.source = source

    def __str__(self):
        return textwrap.dedent(
            """
            Class:\t{cls}
            {type}:\t{description}
            Line:\t{line}
            Source:\t{source}
            """.format(cls=self.cls, type=self.type.title(), description=self.description, line=self.line, source=self.source.strip())
        )


class Shader(object):
    vertex = GL.GL_VERTEX_SHADER
    fragment = GL.GL_FRAGMENT_SHADER

    error_parsers =[
        # ATI
        # ERROR: 0:131: '{' : syntax error parse error
        re.compile(r'(?P<type>\w+):\s+(\d+):(?P<line>\d+):\s+(?P<description>.*)', flags=re.I),

        # Nvidia
        # 0(7): error C1008: undefined variable "MV"
        re.compile(r'\d+(?P<line>\d+):\s+(?P<type>\w)\s+\w:\s+(?P<description>.*)', flags=re.I),

        # Nouveau
        # 0:28(16): error: syntax error, unexpected ')', expecting '('
        re.compile(r'\d+:\d+\((?P<line>\d+)\):\s+(?P<type>\w):\s+(?P<description>.*)', flags=re.I),
    ]

    @classmethod
    def _parse_errors(cls, shader, errors):
        def parse(error, source):
            for parser in Shader.error_parsers:
                match = parser.match(error)
                if match:
                    line = int(match.group('line'))
                    return ShaderError(
                        cls=cls.__name__,
                        type=match.group('type').lower(),
                        description=match.group('description'),
                        line=line,
                        source=source[line - 1],
                    )
            raise ValueError('Unknown GLSL error format: {}'.format(error))

        source = shader.source.split('\n')
        lines = errors.strip().split('\n')
        errors = [
            parse(line, source)
            for line in lines
        ]
        return errors

    def __init__(self, type, source):
        self._handle = GL.glCreateShader(type)
        self.type = type
        self.source = source
        self._compile()

    def __del__(self):
        self.delete()

    def delete(self):
        GL.glDeleteShader(self._handle)

    @property
    def handle(self):
        return self._handle

    def _compile(self):
        GL.glShaderSource(self._handle, self.source)
        GL.glCompileShader(self._handle)

        if not GL.glGetShaderiv(self._handle, GL.GL_COMPILE_STATUS):
            errors = GL.glGetShaderInfoLog(self._handle)
            errors = self._parse_errors(self, errors)
            raise ShaderException(errors)


vertex = Shader.vertex
fragment = Shader.fragment

