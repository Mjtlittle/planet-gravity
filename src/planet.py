from vector import Vector

class Planet:
    def __init__(self, position: Vector, mass, radius) -> None:
        self.position = position
        self.velocity = (0,0)
        self.mass = mass
        self.radius = radius
        