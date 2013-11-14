import unittest
import numpy as np
from OpenGL import GL
import omgl
from omgl.tests import setUpModule, tearDownModule

class TestArrayBuffer(unittest.TestCase):

    def test_empty(self):
        b = omgl.array_buffer.empty((2,3), dtype=np.float32)
        # test by setting the data and ensuring not gl exception is raised

    def test_npdata(self):
        data = np.arange(10, dtype=np.float32)
        b = omgl.array_buffer.npdata(data)

        self.assertTrue(np.array_equal(b.data, data), (b.data, data))

        # test the data is there
        gl_data = b.get_data()
        self.assertTrue(np.array_equal(gl_data, data), (gl_data, data))


if __name__ == '__main__':
    from omgl.tests import setUpModule, tearDownModule
    setUpModule()
    unittest.main()
    tearDownModule()
