from math import sin, pi
from engine import GFXDrawShape, TimeIt, clamp
from time import perf_counter
import pygame


#alpha limit 100-170
# if alpha goes above 170 then difference starts at 100
# if given alpha
# if lowerbound + alpha%upperbound


def sinAlpha(alpha, alphaLimit, reverse, dif, normalWaveLenth, midDif):
    if reverse:
        return midDif + sin(alpha*normalWaveLenth + pi/2)*dif/2
    return midDif + sin(alpha*normalWaveLenth - pi/2)*dif/2
    

def modAlpha(alpha, alphaLimit, reverse, dif, *args): #arg0 = lower arg1 = upper
    if reverse:
        return alphaLimit[1] - alpha%(dif)
    return alphaLimit[0] + alpha%(dif)


class TrailTemplate(object):
    def __init__(self, position, startingAngle, whenKill, angleIncrement=0, PolyInfo=None, MinorChanges=(0, 255, True), alphaChangeDuration=None):
        self.position = position[::]
        self.angleMomentum = angleIncrement
        self.angle = startingAngle
        self.whenKill = whenKill
        self.start = perf_counter()
        self.alpha = 255
        self.alphaLimit = MinorChanges[:2]
        self.reverseAlpha = MinorChanges[2]#Alpha min, alpha max, 
        self.PolyInfo = PolyInfo
        
        self.alphaChangeDuration = alphaChangeDuration if alphaChangeDuration else (whenKill, modAlpha)
        self.alphaDif = self.alphaLimit[1] - self.alphaLimit[0]
        self.alphaWaveLength = 2*pi/self.alphaDif
        self.midDif = (self.alphaLimit[1] + self.alphaLimit[0])/2
        

        self.image = GFXDrawShape(*self.PolyInfo, self.angle, alpha=self.alphaChangeDuration[1](
                                        self.alpha, self.alphaLimit, self.reverseAlpha, self.alphaDif, self.alphaWaveLength, self.midDif))
    def isItTimeToKill(self, start, whenKill):
        if TimeIt(whenKill, start):
            return True
        return False



class MotionBlurEffectTrail(TrailTemplate):
    def update(self, dt, TRAILS):
        self.alpha = (perf_counter() - self.start)/self.alphaChangeDuration[0]*self.alphaDif
        
        if not self.isItTimeToKill(self.start, self.whenKill):
            self.angle += self.angleMomentum*dt
            self.image = GFXDrawShape(*self.PolyInfo, self.angle, alpha=self.alphaChangeDuration[1](
                                        self.alpha, self.alphaLimit, self.reverseAlpha, self.alphaDif, self.alphaWaveLength, self.midDif))
            
            return  # Kill or not
        TRAILS.remove(self)
    
class SpriteCircleRadiusTrail(object):
    def __init__(self, position, startingAngle, whenKill, angleIncrement=0, PolyInfo=None, MinorChanges=(0, 255, True), alphaChangeDuration=None):
        self.position = position
        self.angleMomentum = angleIncrement
        self.angle = 0
        self.whenKill = 1000000000
        self.start = perf_counter()
        self.alpha = 255
        self.MinorChanges = MinorChanges