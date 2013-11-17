import unittest
import os.path
import numpy as np
from OpenGL import GL
import omgl
from omgl.tests import setUpModule, tearDownModule

glfw_imported = False

try:
    import cyglfw3 as glfw
    glfw_imported = True
except:
    pass

class TestGLFW_Window(unittest.TestCase):

    def test_creation(self):
        if not glfw_imported:
            return unittest.skip("CyGLFW3 Not present")

        window = omgl.glfw3_window.create((1024,768), 'Hello')
