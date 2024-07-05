from vec3 import Vec3
class Sphere:
    def __init__(self, center: Vec3, radius: float, color: Vec3, spec: float, reflect: float, emmisive: bool = False) -> None:
        self.center = center
        self.radius = radius
        self.color = color
        self.spec = spec
        self.reflect = reflect
        self.emmisive = emmisive