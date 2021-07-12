from engine import *
from Composition import *




class Bullets(object):
    def __init__(self, pointoOject, polygonObject, lifeDuration):
        self.point = pointoOject
        self.polygon = polygonObject
        self.lifeDuration = lifeDuration
    
    def update(self, dt):
        self.point.update(dt)
        self.polygon.update(dt)

        self.position = self.point.position
        self.image = self.polygon.image

class SimpleBulletN(Bullets):
    def __init__(self, lifeDuration, position, velocity, angle, polgonName):
        Bullets.__init__(self, PointObject(position, velocity, angle), PolygonOverviewObject(TEMPLATEPOLYGON[polgonName]), lifeDuration)
