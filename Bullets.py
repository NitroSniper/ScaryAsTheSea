from time import perf_counter
from Composition import PointObject, PolygonOverviewObject, TemplateMaker, GameListPointers
from engine import TimeIt
from time import perf_counter
import pygame



class Bullets(GameListPointers):
    def __init__(self, pointoOject, polygonObject, lifeDuration, addToList=True):
        self.point = pointoOject
        self.polygon = polygonObject
        self.lifeDuration = lifeDuration
        self.spawnTime = perf_counter()

        self.image = self.polygon.image
        self.position = self.point.position
    
        if addToList:
            Bullets.BULLETS.append(self)
    def update(self, dt):
        self.point.update(dt)
        self.polygon.update(dt)

        self.position = self.point.position
        self.image = self.polygon.image

        if TimeIt(self.lifeDuration, self.spawnTime):
            Bullets.BULLETS.remove(self)
    
    def getRect(self):
        return self.image.get_rect(topleft=self.position)
    def getMask(self):
        return pygame.mask.from_surface(self.image)

class SimpleBullet(Bullets):
    def __init__(self, lifeDuration, position, velocity, angle, polygonName):
        Bullets.__init__(self, PointObject(position, velocity, angle), PolygonOverviewObject(TemplateMaker(polygonName, 120, 1)), lifeDuration)
