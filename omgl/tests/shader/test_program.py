import unittest
import os.path
import numpy as np
from OpenGL import GL
import omgl
from omgl.tests import setUpModule, tearDownModule

class TestProgram(unittest.TestCase):

    def test_program_120(self):
        if omgl.gl.glsl_version() > 120:
            return unittest.skip("Legacy profile not being used")

        vs = omgl.vertex_shader.load(os.path.join(os.path.dirname(__file__), 'shader_vertex_120.glsl'))
        fs = omgl.fragment_shader.load(os.path.join(os.path.dirname(__file__), 'shader_fragment_120.glsl'))
        p = omgl.program.create(vs, fs)

    def test_program_150(self):
        if omgl.gl.glsl_version() <= 120:
            return unittest.skip("Legacy profile not being used")

        vs = omgl.vertex_shader.load(os.path.join(os.path.dirname(__file__), 'shader_vertex_150.glsl'))
        fs = omgl.fragment_shader.load(os.path.join(os.path.dirname(__file__), 'shader_fragment_150.glsl'))
        p = omgl.program.create(vs, fs)

    def test_program_duplicate_symbols_120(self):
        if omgl.gl.glsl_version() > 120:
            return unittest.skip("Legacy profile not being used")

        vs = omgl.vertex_shader.load(os.path.join(os.path.dirname(__file__), 'shader_vertex_120.glsl'))
        vs2 = omgl.vertex_shader.load(os.path.join(os.path.dirname(__file__), 'shader_vertex_120.glsl'))
        fs = omgl.fragment_shader.load(os.path.join(os.path.dirname(__file__), 'shader_fragment_120.glsl'))
        with self.assertRaises(omgl.program.ProgramException):
            p = omgl.program.create(vs, fs, vs2)

    def test_program_duplicate_symbols_150(self):
        if omgl.gl.glsl_version() <= 120:
            return unittest.skip("Legacy profile not being used")

        vs = omgl.vertex_shader.load(os.path.join(os.path.dirname(__file__), 'shader_vertex_150.glsl'))
        vs2 = omgl.vertex_shader.load(os.path.join(os.path.dirname(__file__), 'shader_vertex_150.glsl'))
        fs = omgl.fragment_shader.load(os.path.join(os.path.dirname(__file__), 'shader_fragment_150.glsl'))
        with self.assertRaises(omgl.program.ProgramException):
            p = omgl.program.create(vs, fs, vs2)

    def test_program_attribute_values_120(self):
        if omgl.gl.glsl_version() > 120:
            return unittest.skip("Legacy profile not being used")

        vs = omgl.vertex_shader.load(os.path.join(os.path.dirname(__file__), 'shader_vertex_120.glsl'))
        fs = omgl.fragment_shader.load(os.path.join(os.path.dirname(__file__), 'shader_fragment_120.glsl'))
        p = omgl.program.create(vs, fs, in_position=15)
        self.assertEqual(p.attributes['in_position'], 15)

    def test_program_attribute_values_150(self):
        if omgl.gl.glsl_version() <= 120:
            return unittest.skip("Legacy profile not being used")

        vs = omgl.vertex_shader.load(os.path.join(os.path.dirname(__file__), 'shader_vertex_150.glsl'))
        fs = omgl.fragment_shader.load(os.path.join(os.path.dirname(__file__), 'shader_fragment_150.glsl'))
        p = omgl.program.create(vs, fs, in_projection=5, in_model_view=10, in_position=15)
        self.assertEqual(p.attributes['in_projection'], 5)
        self.assertEqual(p.attributes['in_model_view'], 10)
        self.assertEqual(p.attributes['in_position'], 15)

    def test_program_load_120(self):
        if omgl.gl.glsl_version() > 120:
            return unittest.skip("Legacy profile not being used")

        vs = os.path.join(os.path.dirname(__file__), 'shader_vertex_120.glsl')
        fs = os.path.join(os.path.dirname(__file__), 'shader_fragment_120.glsl')
        p = omgl.program.load(vs, fs)

    def test_program_load_150(self):
        if omgl.gl.glsl_version() <= 120:
            return unittest.skip("Legacy profile not being used")

        vs = os.path.join(os.path.dirname(__file__), 'shader_vertex_150.glsl')
        fs = os.path.join(os.path.dirname(__file__), 'shader_fragment_150.glsl')
        p = omgl.program.load(vs, fs)

