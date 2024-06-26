import pygame
from shapes import Sphere
from scene import Scene
from vec3 import Vec3
from math import sqrt, pi, cos, sin
import camera
from lights import Light, PointLight, DirectionalLight

# XXX view direction for spec may not work with moving the camera
# TODO add canvas to viewport

# Camera
vSize = [1, 1]
d = 1
cSize = [100, 100]
bgColor = [0, 0, 0]
scale = 10

myCamera = camera.Camera(Vec3(0, 0, 0), vSize[0], vSize[1], d, cSize[0], cSize[1], bgColor, scale)

# Pygame
pygame.init()
screen = pygame.display.set_mode([myCamera.cWidth * scale, myCamera.cHeight * scale])

# Spheres
spheres: list[Sphere] = []
spheres.append(Sphere(Vec3(0, -1, 3), 1, (255, 0, 0), spec=500, reflective=0.1))
spheres.append(Sphere(Vec3(2, 0, 4), 1, (0, 0, 255), spec=500, reflective=0.1))
spheres.append(Sphere(Vec3(-2, 0, 4), 1, (0, 255, 0), spec=10, reflective=0.1))
spheres.append(Sphere(Vec3(0, -5001, 0), 5000, (255, 255, 0), spec=1000, reflective=0.5))

# Lights
ambientLight: float = 0.2
lights = []
lights.append(PointLight(0.6, Vec3(2, 1, 0)))
lights.append(DirectionalLight(0.2, Vec3(1, 4, 4)))

# Scene
myScene = Scene(spheres, ambientLight, lights)

yaw: float = 0
pitch: float = 0

# Drawing
for i in [1]:
    for cX in range(int(-myCamera.cWidth/2), int(myCamera.cWidth/2)):
        for cY in range(int(-myCamera.cHeight/2), int(myCamera.cHeight/2)):

            viewPortPoint = Vec3(cX * (myCamera.vWidth / myCamera.cWidth), cY * (myCamera.vHeight / myCamera.cHeight), myCamera.focalLength)

            viewPortPoint -= myCamera.position
            rotatedPoint: Vec3 = viewPortPoint

            # Yaw
            rotatedPoint.x = viewPortPoint.x * cos(yaw) - viewPortPoint.z * sin(yaw)
            rotatedPoint.z = viewPortPoint.x * sin(yaw) + viewPortPoint.z * cos(yaw)

            # Pitch
            rotatedPoint.y = viewPortPoint.y * cos(pitch) - viewPortPoint.z * sin(pitch)
            rotatedPoint.z = viewPortPoint.y * sin(pitch) + viewPortPoint.z * cos(pitch)

            rotatedPoint += myCamera.position


            color = myCamera.TraceRay(myCamera.position, rotatedPoint, 1, float("inf"), myScene, 3)
            screenX, screenY = myCamera.CanvasToScreen(cX, cY)
            if myCamera.scale == 1:
                screen.set_at([screenX, screenY], color)
            else:
                pygame.draw.rect(screen, color, pygame.Rect(int(screenX - scale / 2), int(screenY - scale / 2), scale, scale))
    pygame.display.flip()
    yaw = 0
    pitch = 0

while True:
    pass