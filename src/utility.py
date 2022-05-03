from pyglet.gl import *
from pyglet import text, shapes

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

def draw_buttons(window):
    
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

    # render the button
    rectangle = shapes.Rectangle(300, window.height - 100, 100, 50, color=(255, 22, 20))
    rectangle.opacity = 255
    rectangle.draw()
    draw_label(window, text.Label('Test_Label',font_name='Arial',
            font_size=20,
            x=310,
            y=window.height - 120))

    # return to old transforms
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    # disable depth test
    glEnable(GL_DEPTH_TEST)