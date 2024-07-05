from vec3 import Vec3

class Light:
    def __init__(self, intensity: float) -> None:
        self.intensity = intensity

class PointLight(Light):
    def __init__(self, intensity: float, position: Vec3) -> None:
        super().__init__(intensity)
        self.position = position

class DirectionalLight(Light):
    def __init__(self, intensity: float, direction: Vec3) -> None:
        super().__init__(intensity)
        self.direction = direction