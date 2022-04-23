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

# Sun
planets.append(Planet(
    'Sun',
    position=Vector(0,0,0),
    mass=500,
    radius=1,
    texture_path='sun.jpg',
    rotation=0
))

# Mercury
planets.append(Planet(
    'Mercury',
    position=Vector(2,0,2),
    mass=5,
    radius=0.1,
    texture_path='mercury.jpg',
    rotation=0
))

# Venus
planets.append(Planet(
    'Venus',
    position=Vector(3,0,3),
    mass=50,
    radius=0.4,
    texture_path='venus.jpg',
    rotation=0
))

# Earth
planets.append(Planet(
    'Earth',
    position=Vector(4,0,4),
    mass=50,
    radius=0.4,
    texture_path='earth.jpg',
    rotation=0
))

# Mars
planets.append(Planet(
    'Mars',
    position=Vector(5,0,5),
    mass=30,
    radius=0.3,
    texture_path='mars.jpg',
    rotation=0
))

# Jupiter
planets.append(Planet(
    'Jupiter',
    position=Vector(6,0,6),
    mass=100,
    radius=0.8,
    texture_path='jupiter.jpg',
    rotation=0
))

# Saturn
planets.append(Planet(
    'Saturn',
    position=Vector(7,0,7),
    mass=80,
    radius=0.7,
    texture_path='saturn.jpg',
    rotation=0
))

# Neptune
planets.append(Planet(
    'Neptune',
    position=Vector(8,0,8),
    mass=60,
    radius=0.6,
    texture_path='neptune.jpg',
    rotation=0
))

# Uranus
planets.append(Planet(
    'Uranus',
    position=Vector(9,0,9),
    mass=40,
    radius=0.5,
    texture_path='uranus.jpg',
    rotation=0
))

# Pluto
planets.append(Planet(
    'Pluto',
    position=Vector(10,0,10),
    mass=10,
    radius=0.1,
    texture_path='pluto.jpg',
    rotation=0
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
glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )


# TODO: Make them rotate
# TODO: Make them orbit
# TODO: Implement Newtonian physics

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
    # draw_grid()

    # Wireframe mode:
    # glPolygonMode( GL_FRONT_AND_BACK, GL_LINE)

    # Fill mode:
    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

    glColor3f(1,1,1)
    
    for planet in planets:
        glPushMatrix()
        glTranslatef(*planet.position)
        texture = planet.texture
        glEnable(texture.target)
        glBindTexture(texture.target, texture.id)
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        gluQuadricNormals(quadric, GL_SMOOTH)
        gluSphere(quadric, planet.radius, 20, 20)
        glPopMatrix()
        glRotatef(planet.rotation, 0,1,0);
        planet.rotation += .1 % 360
    
    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

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

