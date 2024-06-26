from vec3 import Vec3
class Sphere:
    def __init__(self, center: Vec3, radius: float, color: list[float], spec: float = 1, reflective: float = 0) -> None:
        self.center = center
        self.radius = radius
        self.color = color
        self.spec = spec
        self.reflective = reflective