from engine import GFXDrawShape
from time import perf_counter
from math import pi


def sinAlpha(alpha, alphaLimit, reverse, dif, normalWaveLenth, midDif):
    if reverse:
        return midDif + sin(alpha*normalWaveLenth + pi/2)*dif/2
    return midDif + sin(alpha*normalWaveLenth - pi/2)*dif/2
    

def modAlpha(alpha, alphaLimit, reverse, dif, *args): #arg0 = lower arg1 = upper
    if reverse:
        return alphaLimit[1] - alpha%(dif)
    return alphaLimit[0] + alpha%(dif)



class Point(object):
    def __init__(self, position, velocity, angle):
        self.position = position
        self.velocity = velocity
        self.angle = angle
    
    def update():
        pass

class PolygonInformation(object):
    def __init__(self, verticesNum, radius, color, alphaLimit, alphaShiftDuration, rotation, rotationIncrement, alphaFunc=modAlpha, alphaReverse=False):
        self.verticesNum = verticesNum
        self.radius = radius
        self.color = color
        self.alphaLimit = alphaLimit
        self.alphaShiftDuration = alphaShiftDuration
        self.alphaOverflowFunc = alphaFunc
        self.start = perf_counter()
        self.alphaReverse = alphaReverse

        self.rotation = rotation
        self.rotationIncrement = rotationIncrement
        
        
        self.alphaDifference = alphaLimit[1] - alphaLimit[0]
        self.alphaWaveLength = 2*pi/self.alphaDifference
        self.meanInAlphaLimit = (self.alphaLimit[0] + self.alphaLimit[1])/2

        self.alpha = 0
        self.IMGAlpha = self.alphaOverflowFunc(self.alpha, self.alphaLimit, self.alphaReverse, self.alphaDifference, self.alphaWaveLength, self.meanInAlphaLimit)

        self.image = GFXDrawShape(self.verticesNum, self.radius, self.color, self.rotation, self.IMGAlpha)
    def update(self, dt):
        self.alpha = (perf_counter() - self.start)/self.alphaShiftDuration*self.alphaDifference
        self.IMGAlpha = self.alphaOverflowFunc(self.alpha, self.alphaLimit, self.alphaReverse, self.alphaDifference, self.alphaWaveLength, self.meanInAlphaLimit)
        
        self.rotation = 

