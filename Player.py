import pygame
from Composition import *
from Trails import *



DEFAULT_SPEED = 5
DEFAULT_LIVES = 3
DEFAULT_ANGLE = 3
SIZE = 20
# https://stackoverflow.com/questions/67168804/how-to-make-a-circular-countdown-timer-in-pygame
# https://stackoverflow.com/questions/3436453/calculate-coordinates-of-a-regular-polygons-vertices


class nPlayerObject(object):
    def __init__(self, moveSetKey, dashKey, vertices, pos):
        self.moveSet = moveSetKey
        self.movement = {'UP': False, 'DOWN': False,
                         'LEFT': False, 'RIGHT': False}

        self.position = list(pos)
        self.angle = 0
        self.speed = DEFAULT_SPEED
        self.angleChanges = 0
        # self.polygon = PolygonInformationObject(vertices, 20, (255, 255, 255), (100, 255), 2, 0, 1, sinAlpha)
        self.polygon = PolygonInformationObject(vertices, 20, (3, 207, 252), (255, 255), 1, 0, 1)


        self.trail = TrailInformationObject(MotionBlurTrail, timerDuration=2, spawnTimer=10, target=self)
    def update(self, dt, TRAILS):
        self.angleChanges = 0
        movement = any(move == True for move in self.movement.values())
        if movement:
            self.angleChanges += 5
            if self.movement['UP']:
                self.position[1] -= self.speed*dt
            if self.movement['DOWN']:
                self.position[1] += self.speed*dt
            if self.movement['LEFT']:
                self.position[0] -= self.speed*dt
            if self.movement['RIGHT']:
                self.position[0] += self.speed*dt
        
        self.polygon.update(dt, externalRotationInc=self.angleChanges)
        self.trail.update(TRAILS)
        self.image = self.polygon.image