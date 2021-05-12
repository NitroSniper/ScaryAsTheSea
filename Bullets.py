#Why the fuck can't i draw triangles good do i have to use images... nvm did it

from engine import GFXDrawShapes
from engine import *
from time import perf_counter
dict = {
    'triangleWithCore' : ((3, 1, (255, 255, 255), 1, 255), (3, 0.5, (0, 0 ,0 ), 1, 0), (4, 0.1875, (255, 0, 0), -1, 255))
}

# in theory the 1st polyinfo angle is x and the rest is multiple of x
#https://stackoverflow.com/questions/49835256/correct-way-to-extend-init-in-python-3-from-parent-class
class BulletTemplate(object):
    def update():
        pass

class SimpleBullet(BulletTemplate):
    def __init__(self, size, PolyTemplate, position, velocity, angle, angleIncrement, whenKill, customizeDict=None):
        self.size = size
        self.position = list(position)
        self.velocity = velocity
        self.angle = angle
        self.angleIncrement = angleIncrement
        self.PolyScalar = {}
        self.PolyInfo = {}
        #Now we are making a dict to store each Poly Information
        for index, poly in enumerate(dict[PolyTemplate]):
            self.PolyScalar[index] = (poly[1], poly[3])
            self.PolyInfo[index] = [poly[0], 
                                    self.size*self.PolyScalar[index][0], 
                                    poly[2], 
                                    self.angle*self.PolyScalar[index][1], 
                                    poly[4]]# vertices, sizeScalar, RGB, AngleScalar, Alpha
        self.image = GFXDrawShapes(tuple(self.PolyInfo.values()))

        self.WhenKill = whenKill
        self.start = perf_counter()
        
    def update(self, dt):
        self.angle += self.angleIncrement*dt
        for index, poly in enumerate(self.PolyInfo.values()):
            poly[3] = self.angle*self.PolyScalar[index][1]
        self.image = GFXDrawShapes(tuple(self.PolyInfo.values()))
