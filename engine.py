
from math import sin, cos, pi, radians
from time import perf_counter
import pygame
from pygame import gfxdraw
from inspect import getfullargspec

def Collision(playerInfo, ListofBulletInfo):
    Collide, NearHit = False, False
    for bulletInfo in ListofBulletInfo:
        if playerInfo[0].colliderect(bulletInfo[0]):
            offset = (int(playerInfo[2][0] - bulletInfo[2][0]),
                      int(playerInfo[2][1] - bulletInfo[2][1]))
            if bulletInfo[1].overlap(playerInfo[1], offset):
                Collide = True
    return NearHit, Collide

def RotAngle(angle):
    return angle+90


def RotationBlit(Surface, Image, Position, Angle=0, Alpha=255):
    rotatedIMG = pygame.transform.rotate(Image, Angle)
    rotatedIMG.set_alpha(Alpha)
    Surface.blit(rotatedIMG, (int(Position[0] - rotatedIMG.get_width()/2),
                              int(Position[1] - rotatedIMG.get_height()/2)))


def TimeIt(duration, start, compensation=0):
    return perf_counter() - (start+compensation) > duration

def TrigVectors(angle, velocity, position, dt=1):
    rad = radians(angle)
    position[0] += cos(rad)*velocity
    position[1] += sin(rad)*velocity
    return position

def RotPosition(Image, Angle, Position):
    rotatedIMG = pygame.transform.rotate(Image, Angle)
    return (int(Position[0] - rotatedIMG.get_width()/2),
            int(Position[1] - rotatedIMG.get_height()/2))


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def OutOfBounds(SCREEN_SIZE, PlayerObject, PlayerRect):
    PlayerObject.position = [clamp(PlayerObject.position[0], 0, SCREEN_SIZE[0]), clamp(PlayerObject.position[1], 0, SCREEN_SIZE[1])]
    return PlayerObject



#Maybe Refactor this code at some point
def GFXDrawShape(numPoints, radius, color, angleOffset=0,alpha=255): #
    # print (numPoints, radius, angleOffset)
    surf = pygame.Surface((2*(radius), 2*(radius)), pygame.SRCALPHA)
    angle = 2 * pi / numPoints
    vertices = []
    for i in range(numPoints):
        vertices.append((radius + radius * sin(i * angle + radians(angleOffset)), radius + radius * cos(i * angle + radians(angleOffset))))
    gfxdraw.aapolygon(surf, vertices, color + (alpha,))
    gfxdraw.filled_polygon(surf, vertices, color + (alpha,))
    return surf

def aGFXDrawShapes(listOfGFXDrawShape):
    maxRadius = max(x[1] for x in listOfGFXDrawShape) 
    surf = pygame.Surface((2*(maxRadius), 2*(maxRadius)), pygame.SRCALPHA)
    for numPoints, radius, color, angleOffset, alpha in listOfGFXDrawShape:
        angle = 2 * pi / numPoints
        vertices = []
        for i in range(numPoints):
            vertices.append((maxRadius + radius * sin(i * angle + radians(angleOffset)), maxRadius + radius * cos(i * angle + radians(angleOffset))))
        gfxdraw.aapolygon(surf, vertices, color + (alpha,))
        gfxdraw.filled_polygon(surf, vertices, color + (alpha,))
    # pygame.image.save(surf, 'Hello.png')
    # raise Exception
    return surf


def GFXDrawShapes(listOfGFXDrawShape):
    maxRadius = max(x[1] for x in listOfGFXDrawShape) 
    surf = pygame.Surface((2*(maxRadius), 2*(maxRadius)), pygame.SRCALPHA)
    for numPoints, radius, color, angleOffset, alpha in listOfGFXDrawShape:
        angle = 2 * pi / numPoints
        vertices = []
        for i in range(numPoints):
            vertices.append((maxRadius + radius * sin(i * angle + radians(angleOffset)), maxRadius + radius * cos(i * angle + radians(angleOffset))))
        # gfxdraw.aapolygon(surf, vertices, color + (alpha,))
        gfxdraw.filled_polygon(surf, vertices, color + (alpha,))
    # pygame.image.save(surf, 'Hello.png')
    # raise Exception
    return surf


if __name__ == '__main__':
    GFXDrawShapes([(3, 20, (255, 255, 255)),
                   (3, 25, (255, 255, 255)),
                   (3, 10, (255, 255, 255)),
                   (3, 30, (255, 255, 255)),
                   (3, 14, (255, 255, 255))])