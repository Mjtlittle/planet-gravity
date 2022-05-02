import math

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
    
    def __truediv__(self, scalar):
        return self * (1 / scalar)
        
    def __add__(self, other):
        new = self.copy()
        new.x += other.x
        new.y += other.y
        new.z += other.z
        return new

    def __sub__(self, other):
        new = self.copy()
        new.x -= other.x
        new.y -= other.y
        new.z -= other.z
        return new

    def copy(self):
        return Vector(*self)

    def tuple(self):
        return (self.x, self.y, self.z)

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __abs__(self):
        return self.magnitude()

    def normalize(self):
        return self / abs(self)

    def direction_to(self, other):
        return (self - other).normalize()

    def __iter__(self):
        return iter(self.tuple())
    
    def __repr__(self) -> str:
        return f'<Vector {self.x:.3f}, {self.y:.3f}, {self.z:.3f}>'