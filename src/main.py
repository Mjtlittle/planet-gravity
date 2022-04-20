from pyglet.window import Window, key, mouse
from pyglet import app, event, clock, text, image
from pyglet.gl import *
import math, random

from planet import Planet
from utility import draw_label
from vector import Vector


camera_position = Vector(0, 3, 1)
camera_rotation = Vector(0, 0, 0)
camera_movement_speed = 3
camera_rotation_speed = 0.2

grid_cell_size = 1
grid_cells_side = 50
grid_y_level = 0

planets = []

# Adding specific planets manually on the ecliptic plane
planets.append(Planet(
    'Sun',
    position=Vector(0,0,0),
    mass=100,
    radius=0.5,
    texture_path='sun.jpg'
))

# for i in range(100):
#     planets.append(Planet(
#         position=Vector(
#             random.random()*10 - 5,
#             random.random()*10 - 5,
#             random.random()*10 - 5
#         ), 
#         mass=100, 
#         radius=1
#     ))


window = Window(
    width=640,
    height=480,
    resizable=True,
    caption="Planet Gravity"
)
keys = key.KeyStateHandler()
window.push_handlers(keys)

glEnable(GL_DEPTH_TEST)
glPolygonMode( GL_FRONT_AND_BACK, GL_FILL );


def draw_grid():
    glPushMatrix()
    glLineWidth(1)
    glColor3f(1,1,1)
    glBegin(GL_LINES)

    ww = grid_cell_size * grid_cells_side
    for i in range(grid_cells_side + 1):

        # vertical
        glVertex3f(-ww / 2, grid_y_level, grid_cell_size * i - ww/2)
        glVertex3f(ww / 2, grid_y_level, grid_cell_size * i - ww/2)

        # horizontal
        glVertex3f(grid_cell_size * i - ww/2, grid_y_level, -ww / 2)
        glVertex3f(grid_cell_size * i - ww/2, grid_y_level, ww / 2)

    glEnd()
    glPopMatrix()

@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(80, width / float(height), .1, 1000)
    glMatrixMode(GL_MODELVIEW)
    return event.EVENT_HANDLED

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & mouse.LEFT:
        camera_rotation.y -= dx * camera_rotation_speed
        camera_rotation.x += dy * camera_rotation_speed

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # camera position
    glRotatef(camera_rotation.x, 1, 0, 0)
    glRotatef(camera_rotation.y, 0, 1, 0)
    glTranslatef(*(camera_position * -1))

    # grid
    draw_grid()

    
    # sphere at 0,1,0
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
    glColor3f(1,1,0)
    
    for planet in planets:
        glPushMatrix()
        glTranslatef(*planet.position)
        pic = image.load('textures/'+planet.texture_path)
        texture = pic.get_texture()
        glEnable(texture.target)
        glBindTexture(texture.target, texture.id)
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        gluSphere(quadric, planet.radius, 1000, 1000)
        glPopMatrix()
    
    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL );

    # coordinate overlay
    glColor3f(1.0, 1.0, 1.0)
    label = text.Label(f'X: {camera_position.x:0.2f}, Y: {camera_position.y:0.2f}, Z: {camera_position.z:0.2f}',
        font_name='Arial',
        font_size=12,
        x=10, 
        y=window.height - 10,
        anchor_x='left', 
        anchor_y='top')
    draw_label(window, label)
    label = text.Label(f'FPS: {clock.get_fps():0.0f}',
        font_name='Arial',
        font_size=12,
        x=10, 
        y=window.height - 10 - 12 - 10,
        anchor_x='left', 
        anchor_y='top')
    draw_label(window, label)

def camera_controller(dt):
    dist = dt * camera_movement_speed

    if keys[key.A]:
        camera_position.z -= math.cos(math.radians(camera_rotation.y - 90)) * dist
        camera_position.x += math.sin(math.radians(camera_rotation.y - 90)) * dist
    if keys[key.D]:
        camera_position.z -= math.cos(math.radians(camera_rotation.y - 90)) * -dist
        camera_position.x += math.sin(math.radians(camera_rotation.y - 90)) * -dist
        
    if keys[key.W]:
        camera_position.z -= math.cos(math.radians(camera_rotation.y)) * dist
        camera_position.x += math.sin(math.radians(camera_rotation.y)) * dist

    if keys[key.S]:
        camera_position.z -= math.cos(math.radians(camera_rotation.y)) * -dist
        camera_position.x += math.sin(math.radians(camera_rotation.y)) * -dist

    if keys[key.E]:
        camera_position.y += dist

    if keys[key.Q]:
        camera_position.y -= dist

def update(dt):
    camera_controller(dt)

clock.schedule_interval(update, 1/120.0)
app.run()

