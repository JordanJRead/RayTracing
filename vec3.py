from math import sqrt
class Vec3:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
    def __add__(self, other):
        if type(other) == Vec3:
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        raise TypeError
    
    def __sub__(self, other):
        if type(other) == Vec3:
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        raise TypeError
    
    def __mul__(self, other): # Dot product
        if type(other) == Vec3:
            return self.x * other.x + self.y * other.y + self.z * other.z
        if type(other) in (int, float):
            return Vec3(self.x * other, self.y * other, self.z * other)
        raise TypeError
    
    def __truediv__(self, other):
        if type(other) in (int, float):
            return Vec3(self.x / other, self.y / other, self.z / other)
        raise TypeError
    
    def __abs__(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def from_list(list: list[float]):
        return Vec3(list[0], list[1], list[2])
    
    def __neg__(self):
        return self * -1
        