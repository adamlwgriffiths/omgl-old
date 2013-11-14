from __future__ import absolute_import
from .shader import Shader


def create(source):
    return FragmentShader(source)

def load(filename):
    with open(filename, 'r') as f:
        source = f.read()
        return FragmentShader(source)


class FragmentShader(Shader):
    def __init__(self, source):
        Shader.__init__(self, Shader.fragment, source)
