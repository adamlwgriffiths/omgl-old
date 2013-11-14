import unittest
import numpy as np
from OpenGL import GL
import omgl
from omgl.tests import setUpModule, tearDownModule


class ValidVertexShader(omgl.auto_shader.VertexAutoShader):
    in_position = omgl.auto_shader.AttributeType('vec3', default=2)
    in_texture_coord = omgl.auto_shader.AttributeType('vec2')

    in_projection = omgl.auto_shader.UniformType('mat4')
    in_modelview = omgl.auto_shader.UniformType('mat4')

    ex_texture_coord = omgl.auto_shader.VaryingType('vec2', 'out')

    @omgl.auto_shader.glsl()
    def main(self):
        return """
        gl_Position = in_projection * in_modelview * vec4(in_position, 1.0);
        ex_texture_coord = in_texture_coord;
        """

class ValidFragmentShader(omgl.auto_shader.FragmentAutoShader):
    ex_texture_coord = omgl.auto_shader.VaryingType('vec2', 'in')

    in_texture = omgl.auto_shader.UniformType('sampler2D')

    #out_frag = omgl.auto_shader.VaryingType('out', 'vec4')
    out_frag = omgl.auto_shader.FragType('vec4')

    @omgl.auto_shader.glsl()
    def main(self):
        if omgl.gl.glsl_version() <= 120:
            return """
            gl_FragColor = texture2D(in_texture, ex_texture_coord);
            """
        else:
            return """
            out_frag = texture(in_texture, ex_texture_coord);
            """


class TestAutoShader(unittest.TestCase):
    def test_valid_autoshader(self):
        vs = ValidVertexShader()
        fs = ValidFragmentShader()
        p = omgl.program.create(vs,fs)

    def test_default_attributes(self):
        vs = ValidVertexShader()
        self.assertEqual(vs.in_position, 2)

    def test_override_attributes(self):
        # over-ride the default attribute value
        vs = ValidVertexShader(in_position=3)
        self.assertEqual(vs.in_position, 3)


if __name__ == '__main__':
    from omgl.tests import setUpModule, tearDownModule
    setUpModule()
    unittest.main()
    tearDownModule()
