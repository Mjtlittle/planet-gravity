from vector import Vector

class Planet:
    def __init__(self, name, position: Vector, mass, radius, texture_path) -> None:
        self.name = name
        self.position = position
        self.velocity = (0,0)
        self.mass = mass
        self.radius = radius
        self.texture_path = texture_path
        