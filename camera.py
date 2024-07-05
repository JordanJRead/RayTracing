from vec3 import Vec3
from math import sqrt
from shapes import Sphere
from scene import Scene
from lights import DirectionalLight, PointLight
class Camera:

    def __init__(self, position: Vec3, yaw: float, pitch: float, viewportWidth: int, viewportHeight: int, canvasWidth: int, canvasHeight: int, focalLength: float, scale: int, bgColor: Vec3) -> None:
        self.position = position

        self.yaw = yaw
        self.pitch = pitch

        self.viewportWidth = viewportWidth
        self.viewportHeight = viewportHeight

        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight

        self.focalLength = focalLength

        self.scale = scale

        self.bgColor = bgColor
    
    def CanvasToViewport(self, canvasPoint: list[float, float]):
        return Vec3(self.viewportWidth / self.canvasWidth * canvasPoint[0], self.viewportHeight / self.canvasHeight * canvasPoint[1], self.focalLength)

    def CanvasToScreen(self, canvasPoint: list[float, float]):
        return [int(canvasPoint[0] * self.scale + self.canvasWidth / 2 * self.scale), int(-canvasPoint[1] * self.scale + self.canvasHeight / 2 * self.scale)]

    def TraceRay(self, origin: Vec3, rayDir: Vec3, scene: Scene, minT: float, maxT: float, recursion: int) -> Vec3:
        """Given a ray, returns the color that the ray hits"""
        closestSphere, closestT = self.FindSphereIntersection(origin, rayDir, scene, minT, maxT)
        if closestSphere is None:
            return self.bgColor
        if closestSphere.emmisive:
            return closestSphere.color
        point: Vec3 = rayDir * closestT + origin
        normal: Vec3 = (point - closestSphere.center) / abs(point - closestSphere.center)
        localColor: Vec3 = closestSphere.color * self.ComputeLighting(point, normal, scene, closestSphere)
        if closestSphere.reflect > 0 and recursion > 0:
            viewDir: Vec3 = -rayDir
            reflectDir: Vec3 = normal * 2 * (viewDir * normal) - viewDir
            color: Vec3 = localColor * (1 - closestSphere.reflect) + self.TraceRay(point, reflectDir, scene, 1e-6, maxT, recursion-1) * closestSphere.reflect
            return color
        return localColor
    
    def FindSphereIntersection(self, origin: Vec3, dir: Vec3, scene: Scene, minT: float, maxT: float, findAny: bool = False) -> list[Sphere, float]:
        closestT = float("inf")
        closestSphere = None
        for sphere in scene.spheres:
            a = dir * dir
            b = 2 * (dir * (origin - sphere.center))
            c = (origin - sphere.center) * (origin - sphere.center) - sphere.radius**2
            discriminant = b**2 - 4 * (a * c)
            if discriminant > 0:
                t1 = (-b + sqrt(discriminant)) / (2 * a)
                t2 = (-b - sqrt(discriminant)) / (2 * a)
                if t1 < closestT and t1 < maxT and t1 > minT:
                    closestT = t1
                    closestSphere = sphere
                    if findAny:
                        return closestSphere, closestT
                if t2 < closestT and t2 < maxT and t2 > minT:
                    closestT = t2
                    closestSphere = sphere
                    if findAny:
                        return closestSphere, closestT
        return closestSphere, closestT
    
    def ComputeLighting(self, point: Vec3, normal: Vec3, scene: Scene, sphere: Sphere) -> float:
        intensity: float = scene.ambientLight

        for light in scene.lights:
            maxT: float = None
            lightDir: Vec3 = None

            if type(light) == DirectionalLight:
                # Directional light direction points toward the object, but to compare with the normal (which points away), we flip the light direction
                lightDir = -light.direction

                maxT = float("inf") # Shadow

            elif type(light) == PointLight:
                lightDir = light.position - point
                
                maxT = 1 # Shadow

            closestSphere, closestT = self.FindSphereIntersection(point, lightDir, scene, 1e-4, maxT, True) # Always being hit?
            if type(closestSphere) == None:
                continue

            lightDir = lightDir / abs(lightDir)

            # Diffusue
            normalDotLight: float = normal * lightDir
            if normalDotLight > 0:
                intensity += light.intensity * normalDotLight

            # Specular
            if sphere.spec != -1:
                reflectDir = normal * 2 * (normalDotLight) - lightDir    # Pointing away from sphere
                
                # cos theta = a*b / abs(a) * abs(b)
                viewDir: Vec3 = self.position - point
                viewDir = viewDir / abs(viewDir)
                reflectDotView: float = reflectDir * viewDir
                if reflectDotView >= 0:
                    cosAngle = (reflectDir * viewDir)
                    intensity += cosAngle**sphere.spec * light.intensity

        if intensity > 1:
            intensity = 1
        return intensity if intensity > 0 else 0