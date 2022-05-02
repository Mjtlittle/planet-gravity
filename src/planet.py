from vector import Vector
from pyglet import image

class Planet:
    def __init__(self, name, position: Vector, velocity: Vector, mass=10, radius=1, texture_path="testing.jpg", color=(1,1,1)) -> None:
        self.name = name
        
        self.position = position
        self.velocity = velocity
        
        self.mass = mass
        self.radius = radius
        self.rotation = 0

        self.texture_path = texture_path
        self.texture = image.load('textures/' + self.texture_path).get_texture()
    
        self.trail = []
        self.color = color

    def try_mark_trail(self, distance=10):

        # mark tail if none exist yet
        if (len(self.trail) == 0):
            self.mark_trail()
            return

        # otherwise check distance
        dist = abs(self.trail[-1] - self.position)
        if (dist >= min(distance, self.radius)):
            self.mark_trail()

    def mark_trail(self):
        pos = self.position.copy()
        self.trail.append(pos)

    def limit_trail(self, length=50):
        self.trail = self.trail[-length:]

        