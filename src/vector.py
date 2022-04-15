class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def Zero():
        return Vector(0, 0, 0)
    
    def __mul__(self, scalar):
        new = self.copy()
        new.x *= scalar
        new.y *= scalar
        new.z *= scalar
        return new

    def copy(self):
        return Vector(*self)

    def tuple(self):
        return (self.x, self.y, self.z)

    def __iter__(self):
        return iter(self.tuple())