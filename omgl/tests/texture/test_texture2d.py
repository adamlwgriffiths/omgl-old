import unittest
import os.path
import numpy as np
from OpenGL import GL
import omgl
from omgl.tests import setUpModule, tearDownModule

class TestTexture3D(unittest.TestCase):

    def texture_auto(self, size, dtype):
        data = np.arange(32*32*size, dtype=dtype)
        data.shape = (32,32,size)
        t = omgl.texture2d.create(data)
        actual = t.get_data()
        self.assertTrue(np.array_equal(actual, data), (size, actual, data))
        return t

    #
    # Float 16
    #
    def test_texture_auto_f16_r(self):
        # NOTE: This test FAILS because PyOpenGL doesn't define GL_HALF_FLOAT
        self.texture_auto(1, np.float16)

    def test_texture_auto_f16_rg(self):
        # NOTE: This test FAILS because PyOpenGL doesn't define GL_HALF_FLOAT
        self.texture_auto(2, np.float16)

    def test_texture_auto_f16_rgb(self):
        # NOTE: This test FAILS because PyOpenGL doesn't define GL_HALF_FLOAT
        self.texture_auto(3, np.float16)

    def test_texture_auto_f16_rgba(self):
        # NOTE: This test FAILS because PyOpenGL doesn't define GL_HALF_FLOAT
        self.texture_auto(4, np.float16)

    #
    # Float 32
    #
    def test_texture_auto_f32_r(self):
        self.texture_auto(1, np.float32)

    def test_texture_auto_f32_rg(self):
        self.texture_auto(2, np.float32)

    def test_texture_auto_f32_rgb(self):
        self.texture_auto(3, np.float32)

    def test_texture_auto_f32_rgba(self):
        self.texture_auto(4, np.float32)

    #
    # Uint 8
    #
    def test_texture_auto_ui8_r(self):
        self.texture_auto(1, np.uint8)

    def test_texture_auto_ui8_rg(self):
        self.texture_auto(2, np.uint8)

    def test_texture_auto_ui8_rgb(self):
        self.texture_auto(3, np.uint8)

    def test_texture_auto_ui8_rgba(self):
        self.texture_auto(4, np.uint8)

    #
    # Uint 16
    #
    def test_texture_auto_ui16_r(self):
        self.texture_auto(1, np.uint16)

    def test_texture_auto_ui16_rg(self):
        self.texture_auto(2, np.uint16)

    def test_texture_auto_ui16_rgb(self):
        self.texture_auto(3, np.uint16)

    def test_texture_auto_ui16_rgba(self):
        self.texture_auto(4, np.uint16)

    #
    # Uint 32
    #
    def test_texture_auto_ui32_r(self):
        self.texture_auto(1, np.uint32)

    def test_texture_auto_ui32_rg(self):
        self.texture_auto(2, np.uint32)

    def test_texture_auto_ui32_rgb(self):
        self.texture_auto(3, np.uint32)

    def test_texture_auto_ui32_rgba(self):
        self.texture_auto(4, np.uint32)

    #
    # Int 8
    #
    def test_texture_auto_i8_r(self):
        self.texture_auto(1, np.int8)

    def test_texture_auto_i8_rg(self):
        self.texture_auto(2, np.int8)

    def test_texture_auto_i8_rgb(self):
        self.texture_auto(3, np.int8)

    def test_texture_auto_i8_rgba(self):
        self.texture_auto(4, np.int8)

    #
    # Int 16
    #
    def test_texture_auto_i16_r(self):
        self.texture_auto(1, np.int16)

    def test_texture_auto_i16_rg(self):
        self.texture_auto(2, np.int16)

    def test_texture_auto_i16_rgb(self):
        self.texture_auto(3, np.int16)

    def test_texture_auto_i16_rgba(self):
        self.texture_auto(4, np.int16)

    #
    # Int 32
    #
    def test_texture_auto_i32_r(self):
        self.texture_auto(1, np.int32)

    def test_texture_auto_i32_rg(self):
        self.texture_auto(2, np.int32)

    def test_texture_auto_i32_rgb(self):
        self.texture_auto(3, np.int32)

    def test_texture_auto_i32_rgba(self):
        self.texture_auto(4, np.int32)


    def test_texture_auto_invalid(self):
        data = np.arange(32*32*4, dtype=np.int16)
        with self.assertRaises(ValueError):
            t = omgl.texture2d.create(data)

    def test_default_min_filter(self):
        data = np.arange(32*32*4, dtype=np.float32)
        data.shape = (32,32,4)
        t = omgl.texture2d.create(data, min_filter=GL.GL_NEAREST)
        self.assertEqual(t.min_filter, GL.GL_NEAREST)
        with t:
            filter = GL.glGetTexParameteriv(t.target, GL.GL_TEXTURE_MIN_FILTER)
            self.assertEqual(t.min_filter, filter)

    def test_default_mag_filter(self):
        data = np.arange(32*32*4, dtype=np.float32)
        data.shape = (32,32,4)
        t = omgl.texture2d.create(data, mag_filter=GL.GL_NEAREST)
        self.assertEqual(t.mag_filter, GL.GL_NEAREST)
        with t:
            filter = GL.glGetTexParameteriv(t.target, GL.GL_TEXTURE_MAG_FILTER)
            self.assertEqual(t.mag_filter, filter)

    def test_default_wrap_s(self):
        data = np.arange(32*32*4, dtype=np.float32)
        data.shape = (32,32,4)
        t = omgl.texture2d.create(data, wrap_s=GL.GL_CLAMP_TO_EDGE)
        self.assertEqual(t.wrap_s, GL.GL_CLAMP_TO_EDGE)
        with t:
            filter = GL.glGetTexParameteriv(t.target, GL.GL_TEXTURE_WRAP_S)
            self.assertEqual(t.wrap_s, filter)

    def test_default_wrap_t(self):
        data = np.arange(32*32*4, dtype=np.float32)
        data.shape = (32,32,4)
        t = omgl.texture2d.create(data, wrap_t=GL.GL_CLAMP_TO_EDGE)
        self.assertEqual(t.wrap_t, GL.GL_CLAMP_TO_EDGE)
        with t:
            filter = GL.glGetTexParameteriv(t.target, GL.GL_TEXTURE_WRAP_T)
            self.assertEqual(t.wrap_t, filter)
