import sys
import OpenGL.GLUT as GLUT

window = None

def setUpModule():
    global window
    if not window:
        GLUT.glutInit(sys.argv)
        GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGBA | GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(1024, 768)
        window = GLUT.glutCreateWindow("OMGL (GLUT)")

def tearDownModule():
    global window
    GLUT.glutDestroyWindow(window)
    window = None
