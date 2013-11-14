import unittest
import numpy as np
from OpenGL import GL
import omgl
from omgl.tests import setUpModule, tearDownModule

class TestElementBuffer(unittest.TestCase):
    def test_empty(self):
        b = omgl.element_buffer.empty((2,3), dtype=np.float32)
        # test by setting the data and ensuring not gl exception is raised

    def test_npdata(self):
        data = np.arange(10, dtype=np.float32)
        b = omgl.element_buffer.npdata(data)

        self.assertTrue(np.array_equal(b.data, data), (b.data, data))

        # test the data is there
        gl_data = b.get_data()
        self.assertTrue(np.array_equal(gl_data, data), (gl_data, data))

    def test_draw_preset(self):
        data = np.ones((1,), dtype=[('triangles', np.float32, 6)])
        b = omgl.element_buffer.npdata(data)

        # complex dtype means we can't use array_equal
        self.assertTrue(all(b.data == data))

        b.draw('triangles', GL.GL_TRIANGLES)

    def test_draw_preset(self):
        data = np.ones((1,), dtype=[('triangles', np.float32, 6)])
        b = omgl.element_buffer.npdata(data, polygons={'triangles': GL.GL_TRIANGLES})

        # complex dtype means we can't use array_equal
        self.assertTrue(all(b.data == data))

        b.draw()


if __name__ == '__main__':
    from omgl.tests import setUpModule, tearDownModule
    setUpModule()
    unittest.main()
    tearDownModule()
