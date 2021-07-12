
import pygame
from Composition import *
from Trails import *


DEFAULT_SPEED = 5
DEFAULT_LIVES = 3
DEFAULT_ANGLE = 3
SIZE = 20
# https://stackoverflow.com/questions/67168804/how-to-make-a-circular-countdown-timer-in-pygame
# https://stackoverflow.com/questions/3436453/calculate-coordinates-of-a-regular-polygons-vertices


class PlayerObjectN(object):
    def __init__(self, moveSetKey, dashKey, vertices, pos):
        self.moveSet = moveSetKey
        self.movement = {'UP': False, 'DOWN': False,
                         'LEFT': False, 'RIGHT': False}

        self.position = list(pos)
        self.angle = 0
        self.speed = DEFAULT_SPEED
        self.angleChanges = 0
        self.movementAngle = 5
        # self.polygon = PolygonInformationObject(vertices, 20, (255, 255, 255), (100, 255), 2, 0, 1, sinAlpha)
        self.polygonArguments = {
            'verticesNum': vertices,
            'radius': 20,
            'color': (3, 207, 252),
            'alphaLimit': (255, 255),
            'alphaShiftDuration': 1,
            'rotationSpeed': 1,
            'rotationIncrementSpeed': 0}
        self.polygon = PolygonOverviewObject((self.polygonArguments,))

        self.trailArguments = {
            'trailObject': MotionBlurTrail,
            'timerDuration': 0.05,
            'spawnTimer': 0.5,
            'target': self,
            'changesToPolygon': ({'rotationSpeed': 6, 'alphaLimit': (0, 255), 'alphaShiftDuration': 1, 'alphaOverflowFunc': sinAlpha, 'alphaReverse': True},)
        }

        self.trail = TrailOverviewObject(**self.trailArguments)

    def update(self, dt, TRAILS):
        self.angleChanges = 0
        self.isMovement = any(move == True for move in self.movement.values())
        if self.isMovement:
            self.angleChanges += self.movementAngle
            if self.movement['UP']:
                self.position[1] -= self.speed*dt
            if self.movement['DOWN']:
                self.position[1] += self.speed*dt
            if self.movement['LEFT']:
                self.position[0] -= self.speed*dt
            if self.movement['RIGHT']:
                self.position[0] += self.speed*dt

        self.trail.update(TRAILS)
        self.polygon.update(dt, externalRotationInc=self.angleChanges)
        self.image = self.polygon.image
    
