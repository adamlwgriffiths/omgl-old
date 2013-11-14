import unittest
import numpy as np
from OpenGL import GL
import omgl
from omgl.tests import setUpModule, tearDownModule


class ValidVertexShader(omgl.auto_shader.VertexAutoShader):
    in_position = omgl.auto_shader.AttributeType('vec3', default=2, glsl_gt=120)
    in_texture_coord = omgl.auto_shader.AttributeType('vec2', glsl_gt=120)

    in_projection = omgl.auto_shader.UniformType('mat4', glsl_gt=120)
    in_modelview = omgl.auto_shader.UniformType('mat4', glsl_gt=120)

    ex_texture_coord = omgl.auto_shader.VaryingType('vec2', 'out', glsl_gt=120)

    @omgl.auto_shader.glsl(name='main', glsl_lteq=120)
    def main_120(self):
        return """
        gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;
        gl_FrontColor = gl_Color;
        """

    @omgl.auto_shader.glsl(name='main', glsl_gt=120)
    def main_150(self):
        return """
        gl_Position = in_projection * in_modelview * vec4(in_position, 1.0);
        ex_texture_coord = in_texture_coord;
        """


class ValidFragmentShader(omgl.auto_shader.FragmentAutoShader):
    ex_texture_coord = omgl.auto_shader.VaryingType('vec2', 'in', glsl_gt=120)

    in_texture = omgl.auto_shader.UniformType('sampler2D')

    #out_frag = omgl.auto_shader.VaryingType('out', 'vec4')
    out_frag = omgl.auto_shader.FragType('vec4')

    @omgl.auto_shader.glsl('vec2', ['in vec4 variable', 'float f'])
    def test(self):
        return """
        // im a test function
        return variable.xy * f;
        """

    @omgl.auto_shader.glsl()
    def main(self):
        if omgl.gl.glsl_version() <= 120:
            return """
            test(vec4(1.0,1.0,1.0,1.0), 1.0);
            gl_FragColor = texture2D(in_texture, gl_TexCoord[0].st);
            """
        else:
            return """
            test(vec4(1.0,1.0,1.0,1.0));
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
