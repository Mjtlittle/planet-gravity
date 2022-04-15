from pyglet.gl import *
from pyglet import text

def draw_label(window, label):
    
    # enable depth test
    glDisable(GL_DEPTH_TEST)

    # goto to screen space transforms
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, window.width, 0, window.height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # render the text
    label.draw()

    # return to old transforms
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    # disable depth test
    glEnable(GL_DEPTH_TEST)