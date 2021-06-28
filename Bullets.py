from engine import *

class Bullets(object):
    def __init__(self, pointoOject, polygonObject):
        self.point = pointoOject
        self.polygon = polygonObject
    
    def update(self, dt):
        self.point.update(dt)
        self.polygon.update(dt)

        self.postion = self.point.position
        self.image = self.polygon.image