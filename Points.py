from engine import TrigVectors
class PointObject(object):
    def __init__(self, position, velocity, angle):
        self.position = list(position)
        self.velocity = velocity
        self.angle = angle

    def update(self, dt):
        self.position = TrigVectors(
            self.angle, self.velocity, self.position, dt)

    def copy(self):
        return PointObject(self.position[:], self.velocity, self)