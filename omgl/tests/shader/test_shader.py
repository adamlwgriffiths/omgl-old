import unittest
import os.path
import numpy as np
from OpenGL import GL
import omgl
from omgl.tests import setUpModule, tearDownModule

class TestShader(unittest.TestCase):

    def test_vertex_shader_120(self):
        if omgl.gl.glsl_version() > 120:
            return unittest.skip("Legacy profile not being used")

        source = """
        attribute vec3 in_position;
        void main()
        {
            gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * vec4(in_position, 1.0);
            gl_FrontColor = gl_Color;
        }
        """
        s = omgl.shader.create(omgl.shader.vertex, source)

    def test_invalid_vertex_shader_120(self):
        if omgl.gl.glsl_version() > 120:
            return unittest.skip("Legacy profile not being used")

        source = """
        void main()
        {
            gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * vec4(in_position, 1.0);
            gl_FrontColor = gl_Color;
        }
        """
        with self.assertRaises(omgl.shader.ShaderException):
            s = omgl.shader.create(omgl.shader.vertex, source)

    def test_vertex_shader_150(self):
        if omgl.gl.glsl_version() <= 120:
            return unittest.skip("Core profile not being used")

        source = """
        in mat4 in_projection;
        in mat4 in_model_view;
        in vec3 in_position;

        void main()
        {
            gl_Position = in_projection * in_model_view * vec4(in_position, 1.0);
            gl_FrontColor = gl_Color;
        }
        """
        s = omgl.shader.create(omgl.shader.vertex, source)

    def test_invalid_vertex_shader_150(self):
        if omgl.gl.glsl_version() <= 120:
            return unittest.skip("Core profile not being used")

        source = """
        void main()
        {
            gl_Position = in_projection * in_model_view * vec4(in_position, 1.0);
            gl_FrontColor = gl_Color;
        }
        """
        with self.assertRaises(omgl.shader.ShaderException):
            s = omgl.shader.create(omgl.shader.vertex, source)

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
        s = omgl.shader.create(omgl.shader.fragment, source)

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
            s = omgl.shader.create(omgl.shader.fragment, source)

    def test_fragment_shader_150(self):
        if omgl.gl.glsl_version() <= 120:
            return unittest.skip("Core profile not being used")

        source = """
        in vec2 in_texture_coord;
        uniform sampler2D in_texture;
        out vec3 out_frag;

        void main()
        {
            out_frag = texture2D(in_texture, in_texture_coord.st);
        }
        """
        s = omgl.shader.create(omgl.shader.fragment, source)

    def test_invalid_fragment_shader_150(self):
        if omgl.gl.glsl_version() <= 120:
            return unittest.skip("Core profile not being used")

        source = """
        void main()
        {
            out_frag = texture2D(in_texture, in_texture_coord.st);
        }
        """
        with self.assertRaises(omgl.shader.ShaderException):
            s = omgl.shader.create(omgl.shader.fragment, source)

    def test_vertex_shader_file_120(self):
        if omgl.gl.glsl_version() > 120:
            return unittest.skip("Legacy profile not being used")
        filename = os.path.join(os.path.dirname(__file__), 'shader_vertex_120.glsl')
        s = omgl.shader.load(omgl.shader.vertex, filename)

    def test_vertex_shader_file_150(self):
        if omgl.gl.glsl_version() <= 120:
            return unittest.skip("Core profile not being used")
        filename = os.path.join(os.path.dirname(__file__), 'shader_vertex_150.glsl')
        s = omgl.shader.load(omgl.shader.vertex, filename)

    def test_fragment_shader_file_120(self):
        if omgl.gl.glsl_version() > 120:
            return unittest.skip("Legacy profile not being used")
        filename = os.path.join(os.path.dirname(__file__), 'shader_fragment_120.glsl')
        s = omgl.shader.load(omgl.shader.fragment, filename)

    def test_fragment_shader_file_150(self):
        if omgl.gl.glsl_version() <= 120:
            return unittest.skip("Core profile not being used")
        filename = os.path.join(os.path.dirname(__file__), 'shader_fragment_150.glsl')
        s = omgl.shader.load(omgl.shader.fragment, filename)


