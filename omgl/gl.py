import re
from OpenGL import GL
from .utilities import memoize

PROFILE_LEGACY = 1
PROFILE_CORE = 2

def map_enums(enum_dict):
    result = {}
    for key, value in enum_dict.iteritems():
        try:
            result[getattr(GL, key)] = value
        except AttributeError:
            pass
    return result

def profile():
    return PROFILE_CORE if gl_version() >= (3,) else PROFILE_LEGACY

@memoize
def gl_version():
    # version is guaranteed to be 'MAJOR.MINOR<XXX>'
    # there can be a 3rd version
    # split on full stops, spaces and dashes
    # take the first two values
    string = GL.glGetString(GL.GL_VERSION)
    string = re.split(r'[\.\s\-]', string)[:2]
    return tuple(map(int, string))

@memoize
def glsl_version():
    string = GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION)
    string = string.replace('.', '')
    return int(string)
