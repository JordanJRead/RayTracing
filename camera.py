from vec3 import Vec3
from shapes import Sphere
from lights import PointLight, DirectionalLight, Light
from scene import Scene
from math import sqrt

class Camera:
    """
    Class that holds properties and functions relating to the viewport, canvas, and screen
    """
    def __init__(self, position: Vec3, vWidth: int, vHeight: int, focalLength: int, cWidth: int, cHeight: int, bgColor: list[float], scale: int = 1) -> None:
        self.position = position
        
        # Viewport
        self.vWidth = vWidth
        self.vHeight = vHeight
        self.focalLength = focalLength

        # Canvas
        self.cWidth = cWidth
        self.cHeight = cHeight

        # Screen
        self.bgColor = bgColor

        self.scale = scale

    def RaySphereIntersect(self, point: Vec3, dir: Vec3, sphere: Sphere):
        """
        Returns the t-values of a sphere-ray intersection
        """
        r = sphere.radius
        CO = point - sphere.center

        a = dir * dir
        b = 2 * (CO * dir)
        c = CO * CO - r * r

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return float("inf"), float("inf")
        
        t1 = (-b + sqrt(discriminant)) / (2 * a)
        t2 = (-b - sqrt(discriminant)) / (2 * a)
        return t1, t2
    
    def CanvasToScreen(self, cX: int, cY: int):
        """
        Converts a pixel on the canvas (XY centered on origin) to a point on the screen ((0, 0) in top left)
        """
        screenX = (cX + self.cWidth / 2) * self.scale
        screenY = (-cY + self.cWidth / 2) * self.scale
        return [int(screenX), int(screenY)]
    
    def ClosestIntersection(self, point, dir: Vec3, t_min: float, t_max: float, scene: Scene):
        """
        Given a ray, gives the closest sphere intersection and t-value of the intersection
        """
        closest_t = float("inf")
        closest_sphere = None
        for sphere in scene.spheres:
            t1, t2 = self.RaySphereIntersect(point, dir, sphere)
            if t1 < closest_t and t_min <= t1 <= t_max:
                closest_t = t1
                closest_sphere = sphere
            if t2 < closest_t and t_min <= t2 <= t_max:
                closest_t = t2
                closest_sphere = sphere
        return closest_sphere, closest_t

    def ReflectRay(self, R, N):
        return  N * 2 * (N * R) - R

    def TraceRay(self, start: Vec3, dir: Vec3, t_min: float, t_max: float, scene: Scene, recursion: int):
        """
        Returns the color of a sphere hit by a ray given by a direction
        """
        closest_sphere, closest_t = self.ClosestIntersection(start, dir, t_min, t_max, scene)

        if closest_sphere is None:
            return self.bgColor
        
        point = start + dir * closest_t
        normal = (point - closest_sphere.center) / abs(point - closest_sphere.center)
        intensity = self.ComputeLighting(point, normal, -dir, closest_sphere.spec, scene)
        localColor = [x * intensity for x in closest_sphere.color]

        if recursion <= 0 or closest_sphere.reflective <= 0:
            return localColor
        else:
            R = self.ReflectRay(-dir, normal)
            reflectedColor = self.TraceRay(point, R, 1e-6, float("inf"), scene, recursion-1)

            weightedLocalColor = [x * (1 - closest_sphere.reflective) for x in localColor]
            weightedReflectedColor = [x * closest_sphere.reflective for x in reflectedColor]

            return [x + y for x, y in zip(weightedLocalColor, weightedReflectedColor)]
    
    def ComputeLighting(self, point: Vec3, normal: Vec3, viewDir: Vec3, spec: float, scene: Scene):
        """
        Computes the intensity of light hittin a point
        """
        intensity = scene.ambientLight

        # Point and directional light directions
        for light in scene.lights:
            lightDir = None
            t_max = None

            if type(light) == PointLight:
                lightDir = light.position - point
                t_max = 1

            elif type(light) == DirectionalLight:
                lightDir = light.direction
                t_max = float("inf")
            
            # Shadow check
            blocking_object, blocking_t = self.ClosestIntersection(point, lightDir, 1e-6, t_max, scene)
            if blocking_object is not None:
                continue

            # Diffuse lighting
            nDotL = lightDir * normal
            if nDotL > 0:
                intensity += light.intensity * nDotL / (abs(normal) * abs(lightDir))

            # Specular
            if spec != 1:
                reflectedDir = normal * 2 * nDotL - lightDir
                rDotV = reflectedDir * viewDir
                if rDotV > 0:
                    intensity += light.intensity * (rDotV / abs(reflectedDir * abs(viewDir)))**spec

        return intensity if intensity <= 1 else 1