from scene import Scene
from camera import Camera
from lights import DirectionalLight, PointLight, Light
from vec3 import Vec3
from shapes import Sphere
import pygame
from math import pi, sin, cos

# Camera
cameraPos: Vec3 = Vec3(0, 0, 0)
viewportWidth: int = 1
viewportHeight: int = 1
screenWidth: int = 1000
screenHeight: int = 1000
focalLength: float = 1
scale: int = 10
bgColor: Vec3 = Vec3(20, 20, 20)

myCamera = Camera(cameraPos, 0, 0, viewportWidth, viewportHeight, int(screenWidth / scale), int(screenHeight / scale), focalLength, scale, bgColor = bgColor)

# Lights
ambientLight: float = 0.2
lights = []
lights.append(PointLight(0.6, Vec3(2, 1, 0)))
lights.append(DirectionalLight(0.2, -Vec3(1, 4, 4) / abs(Vec3(1, 4, 4))))

# Spheres
spheres: list[Sphere] = []
spheres.append(Sphere(Vec3(0, -1, 3), 1, Vec3(255, 0, 0), spec=500, reflect=0.1))
spheres.append(Sphere(Vec3(2, 0, 4), 1, Vec3(0, 0, 255), spec=500, reflect=0.1))
spheres.append(Sphere(Vec3(-2, 0, 4), 1, Vec3(0, 255, 0), spec=10, reflect=0.1))
spheres.append(Sphere(Vec3(0, -5001, 0), 5000, Vec3(255, 255, 0), spec=1000, reflect=0.5))

spheres.append(Sphere(Vec3(2, 1, 0), 0.2, Vec3(255, 255, 255), -1, 0, True))

### Scene
scene: Scene = Scene(spheres, ambientLight, lights)

# Pygame
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True

deltaTime = clock.tick(60)/1000
lastMouse = pygame.mouse.get_pos()
centerRange = 100
while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        myCamera.position = Vec3(myCamera.position.x, myCamera.position.y, myCamera.position.z + 1 * deltaTime)
    
    ### Mouse
    currentMouse = pygame.mouse.get_pos()
    deltaMouse = [currentMouse[0] - lastMouse[0], currentMouse[1] - lastMouse[1]]
    lastMouse = currentMouse

    # y-lock
    if myCamera.pitch > pi/2:
        myCamera.pitch = pi/2
    if myCamera.pitch < -pi/2:
        myCamera.pitch = -pi/2

    # Center mouse
    if currentMouse[0] < centerRange or currentMouse[0] > screenWidth - centerRange or currentMouse[1] < centerRange or currentMouse[1] > screenHeight - centerRange:
        pygame.mouse.set_pos([myCamera.canvasWidth * scale / 2, myCamera.canvasHeight * scale / 2])
        lastMouse = [myCamera.canvasWidth * scale / 2, myCamera.canvasHeight * scale / 2]

    myCamera.yaw -= deltaMouse[0] * deltaTime * 0.01
    myCamera.pitch += deltaMouse[1] * deltaTime * 0.01

    for x in range(-int(screenWidth / scale / 2), int(screenWidth / scale / 2)):
        for y in range(-int(screenHeight / scale / 2), int(screenHeight / scale / 2)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        running = False
            viewportPoint: Vec3 = myCamera.CanvasToViewport([x, y])

            # Rotate camera
            rotatedPoint: Vec3 = Vec3(viewportPoint.x * cos(myCamera.yaw) - viewportPoint.z * sin(myCamera.yaw), viewportPoint.y, viewportPoint.x * sin(myCamera.yaw) + viewportPoint.z * cos(myCamera.yaw))
            rotatedPoint.y = rotatedPoint.y * cos(myCamera.pitch) - rotatedPoint.z * sin(myCamera.pitch)
            rotatedPoint.z = rotatedPoint.y * sin(myCamera.pitch) + rotatedPoint.z * cos(myCamera.pitch)

            color: Vec3 = myCamera.TraceRay(myCamera.position, rotatedPoint, scene, myCamera.focalLength, float("inf"), 3)

            screenPoint: list[float, float] = myCamera.CanvasToScreen([x, y])
            if scale == 1:
                screen.set_at([screenPoint[0], screenPoint[1]], color.ToList())
            else:
                pygame.draw.rect(screen, color.ToList(), pygame.Rect(screenPoint[0] - scale / 2, screenPoint[1] - scale / 2, scale, scale))

    deltaTime = clock.tick(60)/1000
    pygame.display.flip()
    print("rendered")