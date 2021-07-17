
from time import perf_counter
import pygame
from Composition import PolygonOverviewObject, sinAlpha, TrailOverviewObject, GameListPointers
from Trails import MotionBlurTrail
from engine import TimeIt

DEFAULT_SPEED = 5
DEFAULT_LIVES = 3
DEFAULT_ANGLE = 3
SIZE = 20
# https://stackoverflow.com/questions/67168804/how-to-make-a-circular-countdown-timer-in-pygame
# https://stackoverflow.com/questions/3436453/calculate-coordinates-of-a-regular-polygons-vertices
# https://stackoverflow.com/questions/28015400/how-to-fade-color


#to do blinking just do on off on off lol

def fadeToRed(color, percent):

    return (color[0] - (color[0]-255)*percent,
            color[1] - color[1]*percent,
            color[2] - color[2]*percent)


#if we have a color[0] as 233 so 233+22*percent 
class PlayerObject(GameListPointers):
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

        self.lastCollision = perf_counter() - 1
        self.lives = 4
        self.alphaPercent = 1


        self.trail = TrailOverviewObject(**self.trailArguments)
        self.image = self.polygon.image
    def update(self, dt):
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

        rect = self.getRect()
        mask = self.getMask()
        hit = False
        if TimeIt(1, self.lastCollision):
            if not self.lives:
                PlayerObject.PLAYERS.remove(self)
            for bullet in PlayerObject.BULLETS:
                bulletRect = bullet.getRect()
                if rect.colliderect(bulletRect):
                    offset = (int(bullet.position[0] - self.position[0]), int(bullet.position[1] - self.position[1]))
                    if mask.overlap(bullet.getMask(), offset):
                        self.lives -= 1
                        if self.lives < 0:
                            self.lives = 0
                        self.polygon.polygons[0].color = fadeToRed(self.polygon.argsDict[0]['color'], 1 - (self.lives*0.25)) #if you want to make player have multiple polygon change this
        
                        self.lastCollision = perf_counter()
        
        else: #when they are still invincible
            if self.lives > 0:
                percentage = perf_counter() - self.lastCollision
                if (percentage // 0.1)%2: 
                    self.alphaPercent = 1
                else:

                    self.alphaPercent = 0
            else:
                # When Player is about to die
                self.alphaPercent =  max((1 - (perf_counter() - self.lastCollision), 0))
                self.polygon.polygons[0].color = (255, 0, 0)
        

        self.trail.update(PlayerObject.TRAILS)
        self.polygon.update(dt, externalRotationInc=self.angleChanges, alphaPercentage=self.alphaPercent% 1.00001)
        self.image = self.polygon.image
    def getRect(self):
        return self.image.get_rect(topleft=self.position)
    def getMask(self):
        return pygame.mask.from_surface(self.image)
