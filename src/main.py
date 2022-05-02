from pyglet.window import Window, key, mouse
from pyglet import app, event, clock, text
from pyglet.gl import *
import math

from planet import Planet
from utility import draw_label
from vector import Vector


camera_position = Vector(0, 3, 1)
camera_rotation = Vector(0, 0, 0)
camera_movement_speed = 3
camera_fast_speed_scale = 3
camera_rotation_speed = 0.2

grid_cell_size = 1
grid_cells_side = 50
grid_y_level = 0

steps_per_frame = 5
step_resolution = 1
playing = True
show_ui = True

planets = [

    # just for testing
    Planet(
        'fake earth',
        position=Vector(5,5,10),
        velocity=Vector(2,0,0),
        texture_path='earth.jpg',
        color=(0,0.5,1),
        mass=0.5,
        radius=0.5,
    ),
    Planet(
        'fake mars',
        position=Vector(7,7,10),
        velocity=Vector(1.5,1.5,0),
        texture_path='mars.jpg',
        color=(1,0,0),
        mass=0.2,
        radius=0.3,
    ),
    Planet(
        'sun',
        position=Vector(0,0,0),
        velocity=Vector(0,0,0),
        texture_path='sun.jpg',
        color=(1,1,0),
        mass=50,
        radius=2,
    )
]

window = Window(
    width=640 * 2,
    height=480 * 2,
    resizable=True,
    caption="Planet Gravity"
)

glEnable(GL_DEPTH_TEST)
glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

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
def on_mouse_scroll(x, y, scroll_x, scroll_y):

    scroll_y *= -1

    # not the most elegant, same as moving code
    # just fiddled with trig until worked lol
    # pretty sure camera rot is being done wrong

    vert_rot = math.radians(camera_rotation.y + 90)
    ud_rot = math.radians(-camera_rotation.x + 90)

    camera_position.x += scroll_y * math.cos(vert_rot) * math.sin(ud_rot)
    camera_position.z += scroll_y * math.sin(vert_rot) * math.sin(ud_rot)
    
    camera_position.y += scroll_y * math.cos(ud_rot)

keys = key.KeyStateHandler()
def handle_key_press(symbol, modifiers):

    # global def here is annoying, in ideal world 
    # all logic in main would be incapsulated in a class
    global steps_per_frame, playing, show_ui

    # increase or decrease steps per frame with - and =
    if symbol == key.MINUS:
        if steps_per_frame > 0:
            steps_per_frame -= 1
    if symbol == key.EQUAL:
        steps_per_frame += 1

    # toggle playing
    if symbol == key.SPACE:
        playing = not playing
    
    # toggle ui
    if symbol == key.ENTER:
        show_ui = not show_ui

window.push_handlers(keys)
window.push_handlers(on_key_press=handle_key_press)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # camera position
    glRotatef(camera_rotation.x, 1, 0, 0)
    glRotatef(camera_rotation.y, 0, 1, 0)
    glTranslatef(*(camera_position * -1))

    draw_planets()
    if (show_ui):
        draw_grid()
        draw_overlay()

def draw_overlay():
    lines = [
        ('▶ Running' if playing else '⏸ Paused') + ' (space)',
        f'FPS: {clock.get_fps():0.0f}',
        f'Camera XYZ: {camera_position.x:0.2f}, {camera_position.y:0.2f}, {camera_position.z:0.2f}',
        f'Planets: {len(planets)}',
        f'Steps per Frame (-,=): {steps_per_frame}',
        'Toggle UI with enter'
    ]
    
    glColor3f(1.0, 1.0, 1.0)
    for i, line in enumerate(lines):
        label = text.Label(line,
            font_name='Arial',
            font_size=12,
            x=10,
            y=window.height - 10 * (i + 1) - 12 * i,
            anchor_x='left',
            anchor_y='top')
        draw_label(window, label)
    
def draw_grid():
    glPushMatrix()
    glLineWidth(1)
    glColor3f(0.2,0.2,0.2)
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

def draw_planet(planet: Planet):
    glPushMatrix()

    # load the texture
    texture = planet.texture
    glEnable(texture.target)
    glBindTexture(texture.target, texture.id)
    glColor3f(1.0, 1.0, 1.0)

    # transform
    glTranslatef(*planet.position)
    glRotatef(planet.rotation, 0, 1, 0)
    glRotatef(-90,1,0,0); # rotate up right

    # render the sphere
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluQuadricNormals(quadric, GL_SMOOTH)
    gluSphere(quadric, planet.radius, 20, 20)

    # disable texture
    glDisable(texture.target)
    
    glPopMatrix()

# todo: maybe just a vector that pokes from surface of each planet
def draw_planet_velocity(planet: Planet):
    glPushMatrix()
    glPopMatrix()

def draw_planet_trail(planet: Planet):
    glPushMatrix()
    glLineWidth(5)
    glColor3f(*planet.color)
    glBegin(GL_LINE_STRIP)
    for pos in planet.trail:
        glVertex3f(*pos)
    glEnd()
    glPopMatrix()

def draw_planets():
    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
    glColor3f(1,1,1)
    
    for planet in planets:
        draw_planet(planet)
        draw_planet_trail(planet)

def step_planets(dt):

    G = 1 # gravitational constant
    
    # calculte each planets velocity
    # (ie. applying forces imposed by other planets)
    # this is bruteforced O(N^2) for now
    for planet in planets:

        # calculate sum of all forces
        F_sum = Vector.Zero()
        for other in planets:

            # skip if same planet
            if other == planet:
                continue
                
            diff = other.position - planet.position
            r = abs(diff)     # distance between

            # skip if planets are in the same position
            # (would result in div by zero)
            if (r == 0):
                continue

            r_hat = diff / r  # unit vector direction to other from planet
            F = r_hat * G * (planet.mass * other.mass) / (r * r)

            F_sum += F

        # apply the sum of all forces
        delta_v = F_sum / planet.mass * dt
        planet.velocity += delta_v
    
    # terminal velocity
    # makes no sense, but saves planets from flying
    # around due to close gravity encounters :)
    t_vel = 5
    for planet in planets:
        if abs(planet.velocity) > t_vel:
            planet.velocity = planet.velocity.normalize() * t_vel

    # rotate each planet
    # idk, made it proportional to mass
    for planet in planets:
        planet.rotation += planet.mass / 500 + 0.2

    # move each planet according to their velocity
    for planet in planets:
        planet.position += planet.velocity * dt

def update_planet_trails():
    for planet in planets:
        planet.try_mark_trail(distance=100)
        planet.limit_trail(100)

def camera_controller(dt):
    dist = dt * camera_movement_speed

    if keys[key.LSHIFT]:
        dist *= camera_fast_speed_scale

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
    if (playing):
        for _ in range(step_resolution * steps_per_frame):
            step_planets(dt / step_resolution)
        update_planet_trails()

clock.schedule_interval(update, 1/120.0)
app.run()

