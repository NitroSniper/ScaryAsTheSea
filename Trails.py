from time import perf_counter
from engine import TimeIt
#this is used as the actual Trail

class TrailObject(object):
    def __init__(self, point, polygon, killTimer):
        self.point = point
        self.polygon = polygon
        self.image = self.polygon.image
        self.position = self.point.position
        self.start = perf_counter()
        self.timer = killTimer


    def update(self, dt, TRAILS):
        self.polygon.update(dt)
        self.point.update(dt)

        self.image = self.polygon.image
        self.position = self.point.position
        if self.timer is not None:
            if TimeIt(self.timer, self.start):
                TRAILS.remove(self)



class MotionBlurTrail(TrailObject):
    def __init__(self, foo, *args, **kwargs):
        super().__init__(*args, **kwargs)
