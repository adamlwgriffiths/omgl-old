import unittest
import numpy as np
from OpenGL import GL
import omgl
from omgl.tests import setUpModule, tearDownModule

class TestBuffer(unittest.TestCase):

    def test_empty(self):
        b = omgl.buffer.empty(GL.GL_ARRAY_BUFFER, (2,3), dtype=np.float32)
        # test by setting the data and ensuring not gl exception is raised

    def test_npdata(self):
        data = np.arange(10, dtype=np.float32)
        b = omgl.buffer.create(GL.GL_ARRAY_BUFFER, data)

        self.assertTrue(np.array_equal(b.data, data), (b.data, data))

        # test the data is there
        gl_data = b.get_data()
        self.assertTrue(np.array_equal(gl_data, data), (gl_data, data))

    def test_sync(self):
        data = np.arange(10, dtype=np.float32)
        b = omgl.buffer.create(GL.GL_ARRAY_BUFFER, data)
        self.assertTrue(np.array_equal(b.data, data), (b.data, data))

        # reverse the data
        data = np.arange(10, 0, step=-1, dtype=np.float32)
        b.data[:] = data
        self.assertTrue(np.array_equal(b.data, data), (b.data, data))

        b.sync()

        # test the data is there
        gl_data = b.get_data()
        self.assertTrue(np.array_equal(gl_data, data), (gl_data, data))

    def test_set_data(self):
        data = np.arange(10, dtype=np.float32)
        b = omgl.buffer.create(GL.GL_ARRAY_BUFFER, data)
        self.assertTrue(np.array_equal(b.data, data), (b.data, data))
        self.assertEqual(b.data.nbytes, 40)

        # reverse the data
        data = np.arange(20, dtype=np.float32)
        b.data = data
        self.assertTrue(np.array_equal(b.data, data), (b.data, data))
        self.assertEqual(b.data.nbytes, 80)

        b.sync()

        # test the data is there
        gl_data = b.get_data()
        self.assertTrue(np.array_equal(gl_data, data), (gl_data, data))

    def test_binding(self):
        b = omgl.buffer.empty(GL.GL_ARRAY_BUFFER, (2,3), dtype=np.float32)
        with b:
            self.assertEqual(GL.glGetInteger(GL.GL_ARRAY_BUFFER_BINDING), b.handle)

if __name__ == '__main__':
    from omgl.tests import setUpModule, tearDownModule
    setUpModule()
    unittest.main()
    tearDownModule()
