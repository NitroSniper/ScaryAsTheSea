import pygame
from math import sin, cos, pi, radians
from engine import GFXDrawShape, TimeIt
from Trails import *
DEFAULT_SPEED = 5
DEFAULT_LIVES = 3
DEFAULT_ANGLE = 3
SIZE = 20
# https://stackoverflow.com/questions/67168804/how-to-make-a-circular-countdown-timer-in-pygame
# https://stackoverflow.com/questions/3436453/calculate-coordinates-of-a-regular-polygons-vertices

class PlayerObject(object):
    def __init__(self, moveSetKey, dashKey, numVertices, position):
        self.moveSet = moveSetKey

        self.position = list(position)
        self.angle = 0
        self.speed = DEFAULT_SPEED

        # dashing = DashClassObject()

        # moveSetKey should be up, down, left, right, dash
        self.movement = {'UP': False, 'DOWN': False,
                         'LEFT': False, 'RIGHT': False}
        self.trailStart = perf_counter()


        #Customizable
        #----------------------------------------------------
        #General
        self.angleIncrement = -1
        self.angleIncrementMoving = -4
        self.color = (110, 1, 95)
        self.color = (3, 207, 252)
        #Trails
        self.trailTimer = 0.01
        self.trailDuration = 3
        self.MinorChanges = (0, 150, True)
        self.alphaChangeDuration = (0.5, sinAlpha)
        self.numSides = numVertices
        #----------------------------------------------------


        # Random Information
        self.centeralAngle = angle = 2 * pi / self.numSides# numPoints
        self.radius = 20

        self.image = GFXDrawShape(self.numSides, self.radius, self.color)
        # self.radius = (30, 30)

        #Trails
        self.trailType = MotionBlurEffectTrail
        


    def update(self, dt, TRAILS):
        totalAngleChange = self.angleIncrement*dt
        movement = any(move == True for move in self.movement.values())
        if movement:
            totalAngleChange += self.angleIncrementMoving*dt
            if self.movement['UP']:
                self.position[1] -= self.speed*dt
            if self.movement['DOWN']:
                self.position[1] += self.speed*dt
            if self.movement['LEFT']:
                self.position[0] -= self.speed*dt
            if self.movement['RIGHT']:
                self.position[0] += self.speed*dt
        
        self.angle += totalAngleChange
        self.image = GFXDrawShape(self.numSides, self.radius, self.color, self.angle)
        
        if TimeIt(self.trailTimer, self.trailStart) and movement:
            self.trailStart = perf_counter()
            TRAILS.append(self.trailType(self.position, self.angle, self.trailDuration, 
                                        totalAngleChange, PolyInfo=(self.numSides, self.radius, self.color), 
                                        MinorChanges=self.MinorChanges, alphaChangeDuration=self.alphaChangeDuration))


    def customize(self, attributeDictionary):
        for key, item in attributeDictionary.items():
            setattr(self, key, item)

    def trails(self):
        pass
    


def updateVertices(radius, angle, numPoints, position=(0,0), angleOffset=0):
    vertices = []
    for i in range(numPoints):
        vertices.append((position[0] + radius * sin(i * (angle+angleOffset)), 
                         position[1] + radius * cos(i * (angle+angleOffset))))
    return vertices







