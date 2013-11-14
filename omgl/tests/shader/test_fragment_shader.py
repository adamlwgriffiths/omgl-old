import unittest
import os.path
import numpy as np
from OpenGL import GL
import omgl
from omgl.tests import setUpModule, tearDownModule

class TestFragmentShader(unittest.TestCase):

    def test_fragment_shader_120(self):
        if omgl.gl.glsl_version() > 120:
            return unittest.skip("Legacy profile not being used")

        source = """
        uniform sampler2D in_texture;

        void main()
        {
            gl_FragColor = texture2D(in_texture, gl_TexCoord[0].st);
        }
        """
        s = omgl.fragment_shader.create(source)

    def test_invalid_fragment_shader_120(self):
        if omgl.gl.glsl_version() > 120:
            return unittest.skip("Legacy profile not being used")

        source = """
        void main()
        {
            gl_FragColor = texture2D(in_texture, gl_TexCoord[0].st);
        }
        """
        with self.assertRaises(omgl.shader.ShaderException):
            s = omgl.fragment_shader.create(source)

    def test_fragment_shader_150(self):
        if omgl.gl.glsl_version() <= 120:
            return unittest.skip("Core profile not being used")

        source = """
        in vec2 in_texture_coord;
        uniform sampler2D in_texture;

        void main()
        {
            gl_FragColor = texture2D(in_texture, in_texture_coord.st);
        }
        """
        s = omgl.fragment_shader.create(source)

    def test_invalid_fragment_shader_150(self):
        if omgl.gl.glsl_version() <= 120:
            return unittest.skip("Core profile not being used")

        source = """
        void main()
        {
            gl_FragColor = texture2D(in_texture, in_texture_coord.st);
        }
        """
        with self.assertRaises(omgl.shader.ShaderException):
            s = omgl.fragment_shader.create(source)

    def test_fragment_shader_file_120(self):
        if omgl.gl.glsl_version() > 120:
            return unittest.skip("Legacy profile not being used")
        filename = os.path.join(os.path.dirname(__file__), 'shader_fragment_120.glsl')
        s = omgl.fragment_shader.load(filename)

    def test_fragment_shader_file_150(self):
        if omgl.gl.glsl_version() <= 120:
            return unittest.skip("Core profile not being used")
        filename = os.path.join(os.path.dirname(__file__), 'shader_fragment_150.glsl')
        s = omgl.fragment_shader.load(filename)



