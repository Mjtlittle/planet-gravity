from pyglet.window import Window, key, mouse
from pyglet import app, event, clock, text, graphics, shapes
from pyglet.gl import *
import math
import ctypes

from planet import Planet
from utility import *
from vector import Vector




camera_position = Vector(0, 3, 1)
camera_rotation = Vector(0, 0, 0)
camera_movement_speed = 3
camera_fast_speed_scale = 3
camera_rotation_speed = 0.2

grid_cell_size = 1
grid_cells_side = 500
grid_y_level = 0

steps_per_frame = 5
step_resolution = 1
playing = True
show_ui = True
sun_only = True

window = Window(
    width=640 * 2,
    height=480 * 2,
    resizable=True,
    caption="Planet Gravity"
)

batch = graphics.Batch()

glEnable(GL_DEPTH_TEST)
glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

# Simulation parameters
demo_system = [
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
        'Sun',
        position=Vector(0,0,0),
        velocity=Vector(0,0,0),
        texture_path='tstar.jpg',
        # color=(1,1,0),
        mass=50,
        radius=2,
    )
]

solar_system = [Planet(
    'Sun',
    position=Vector(0,0,0),
    velocity=Vector(0,0,0),
    mass=70,
    radius=2,
    texture_path='sun.jpg'
),Planet(
    'Mercury',
    position=Vector(8,0,8),
    velocity=Vector(1.8,0,-1.8),
    mass=0.01,
    radius=0.2,
    color=(128/255,127/255,127/255),
    texture_path='mercury.jpg'
),Planet(
    'Venus',
    position=Vector(14,0,14),
    velocity=Vector(1.3,0,-1.3),
    mass=0.5,
    radius=.6,
    color=(194/255,105/255,35/255),
    texture_path='venus.jpg'
),Planet(
    'Earth',
    position=Vector(20,0,20),
    velocity=Vector(1.1,0,-1.1),
    texture_path='earth.jpg',
    color=(64/255,184/255,197/255),
    mass=2,
    radius=0.6,
),Planet(
    'Mars',
    position=Vector(25,0,25),
    velocity=Vector(1,0,-1),
    mass=0.3,
    radius=.5,
    color=(140/255,52/255,36/255),
    texture_path='mars.jpg'
),Planet(
    'Jupiter',
    position=Vector(50,0,50),
    velocity=Vector(.7,0,-.7),
    mass=100,
    radius=1.3,
    color=(163/255,117/255,72/255),
    texture_path='jupiter.jpg'
),Planet(
    'Saturn',
    position=Vector(60,0,60),
    velocity=Vector(.64,0,-.64),
    mass=6,
    radius=1.1,
    color=(255/255,234/255,205/255),
    texture_path='saturn.jpg'
),Planet(
    'Neptune',
    position=Vector(80,0,80),
    velocity=Vector(.56,0,-.56),
    mass=1,
    radius=.9,
    color=(65/255,125/255,211/255),
    texture_path='neptune.jpg'
),Planet(
    'Uranus',
    position=Vector(93,0,93),
    velocity=Vector(.52,0,-.52),
    mass=1,
    radius=.9,
    color=(164/255,212/255,220/255),
    texture_path='uranus.jpg'
),Planet(
    'Pluto',
    position=Vector(89,0,89),
    velocity=Vector(.65,0,-.65),
    mass=0.05,
    radius=0.1,
    color=(105/255,115/255,127/255),
    texture_path='pluto.jpg'
)]

inner_solar_system = solar_system[:5]

alpha_centauri = [
    Planet(
        'Alpha Centauri A',
        position=Vector(-10,0,20),
        velocity=Vector(-.3,0,-.3),
        mass=20,
        radius=3,
        texture_path='gstar.jpg'
    ),Planet(
        'Alpha Centauri B',
        position=Vector(10,0,-10),
        velocity=Vector(.3,0,.3),
        mass=10,
        radius=2,
        texture_path='kstar.jpg'
    ),Planet(
        'Proxima Centauri',
        position=Vector(-30,0,-15),
        velocity=Vector(.5,0,-.1),
        mass=1,
        radius=1,
        texture_path='mstar.jpg'
    )
]

planets = demo_system.copy()


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

    vert_rot = math.radians(camera_rotation.y + 90)
    ud_rot = math.radians(-camera_rotation.x + 90)

    camera_position.x += scroll_y * math.cos(vert_rot) * math.sin(ud_rot)
    camera_position.z += scroll_y * math.sin(vert_rot) * math.sin(ud_rot)
    
    camera_position.y += scroll_y * math.cos(ud_rot)

keys = key.KeyStateHandler()
def handle_key_press(symbol, modifiers):

    # global def here is annoying, in ideal world 
    # all logic in main would be incapsulated in a class
    global steps_per_frame, playing, show_ui, sun_only, planets

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

    # switch planetary systems
    if symbol == key._1:
        planets = solar_system.copy()
    if symbol == key._2:
        planets = inner_solar_system.copy()
    if symbol == key._3:
        planets = alpha_centauri.copy()
    if symbol == key._4:
        planets = demo_system.copy()
    
    # toggle interplanetary gravitation
    if symbol == key.G:
        sun_only = not sun_only

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
        'Toggle Interplanetary Gravity with g: ' + ('[OFF]' if sun_only else '[ON]'),
        'Toggle UI with enter',
        '',
        'Simulations (Enter the number):',
        '1. Solar System',
        '2. Inner Solar System',
        '3. Alpha Centauri (Trinary Star System)',
        '4. Demo System'
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
    glColor3f(0.1,0.1,0.1)
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
    # glColor3f(1,1,1)

    sun = planets[0]
    for planet in planets:
        if (planet.position - sun.position).magnitude() < 1 and planet.name != sun.name:
            planets.remove(planet)
        draw_planet(planet)
        draw_planet_trail(planet)

def step_planets(dt):

    G = 1 # gravitational constant
    
    # calculate each planet's velocity
    # (ie. applying forces imposed by other planets)
    # this is bruteforced O(N^2) for now
    for planet in planets:

        # calculate sum of all forces
        F_sum = Vector.Zero()

        for other in planets:

            # skip if same planet or if gravity disabled between planets
            if other == planet or (sun_only and other.name not in ['Sun','sun','Alpha Centauri A','Alpha Centauri B','Proxima Centauri']):
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


