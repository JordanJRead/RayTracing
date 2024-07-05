from shapes import Sphere
from lights import PointLight, DirectionalLight, Light

class Scene:
    def __init__(self, spheres: list[Sphere], ambientLight: float, lights: list[Light]) -> None:
        self.spheres = spheres
        self.ambientLight = ambientLight
        self.lights = lights