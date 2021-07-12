from Trails import TrailObject
from engine import GFXDrawShape, GFXDrawShapes, TrigVectors, TimeIt
from time import perf_counter
from math import pi, sin

TEMPLATEPOLYGON = {'triangleWithCore': ((3, 1, (255, 255, 255), 1, 255), (3, 0.5, (0, 0, 0), 1, 0), (4, 0.1875, (255, 0, 0), -1, 255))}
TEMPLATEPOLYGON = {'triangleWithCore':({
            'verticesNum': 3,
            'radius': 120,
            'color': (255, 255, 255),
            'alphaLimit': (255, 255),
            'alphaShiftDuration': 1,
            'rotationSpeed': 1,
            'rotationIncrementSpeed': 0},
            {
            'verticesNum': 3,
            'radius': 60,
            'color': (0, 0, 0),
            'alphaLimit': (0, 0),
            'alphaShiftDuration': 1,
            'rotationSpeed': 1,
            'rotationIncrementSpeed': 0},
            {
            'verticesNum': 4,
            'radius': 22.5,
            'color': (255, 0, 0),
            'alphaLimit': (255, 255),
            'alphaShiftDuration': 1,
            'rotationSpeed': -1,
            'rotationIncrementSpeed': 0})}

# https://stackoverflow.com/questions/12467570/python-way-to-speed-up-a-repeatedly-executed-eval-statement


def sinAlpha(alpha, alphaLimit, reverse, dif, normalWaveLenth, midDif):
    if reverse:
        return midDif + sin(alpha*normalWaveLenth + pi/2)*dif/2
    return midDif + sin(alpha*normalWaveLenth - pi/2)*dif/2


def modAlpha(alpha, alphaLimit, reverse, dif, *args):  # arg0 = lower arg1 = upper
    if reverse:
        return alphaLimit[1] - alpha % (dif)
    return alphaLimit[0] + alpha % (dif)

def maxAlpha(alpha, alphaLimit, reverse, dif, *args):
    if reverse:
        val = alphaLimit[1] - alpha
        if val < alphaLimit[0]:
            return alphaLimit[0]
        return alphaLimit[1] - alpha
    #else is not needed
    val = alphaLimit[0] + alpha
    if val > alphaLimit[1]:
        return alphaLimit[1]
    return (alphaLimit[0] + alpha)


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

# rotation normalized
# maybe alpha... nah


class PolygonOverviewObject(object):
    def __init__(self, TupleOfPolygonObjectArgs, currentRotation=0):
        self.argsDict, self.polygons = {}, {}

        for i, argsAsDict in enumerate(TupleOfPolygonObjectArgs):
            self.argsDict[i] = argsAsDict
            self.polygons[i] = PolygonInformationObject(**argsAsDict)

        self.polygonCount = len(TupleOfPolygonObjectArgs)
        self.rotation = currentRotation
        shapeArguments = tuple([polygon.giveGFXDrawArgument(1, self.rotation)
                               for polygon in self.polygons.values()])
        self.image = GFXDrawShapes(shapeArguments)
        self.lastRotationIncrease = 0

    def update(self, dt, externalRotation=0, externalRotationInc=0):
        self.lastRotationIncrease = dt*(externalRotationInc+1)
        self.rotation += self.lastRotationIncrease
        shapeArguments = tuple([polygon.giveGFXDrawArgument(dt, self.rotation)
                               for polygon in self.polygons.values()])
        self.image = GFXDrawShapes(shapeArguments)

    def returnSelfAndEdit(self, tupleOfDictEdit, rotation=0):
        args = []
        for i in range(self.polygonCount):
            default = self.polygons[i].giveInitialArgument()
            if tupleOfDictEdit[i] is not None:
                for key, item in tupleOfDictEdit[i].items():
                    default[key] = item
            args.append(default)
        return PolygonOverviewObject(tuple(args), currentRotation=rotation)
    
    def editSelf(self, tupleOfDictEdit, rotation=0):
        args = []
        for i in range(self.polygonCount):
            default = self.polygons[i].giveInitialArgument()
            if tupleOfDictEdit[i] is not None:
                for key, item in tupleOfDictEdit[i].items():
                    default[key] = item
            args.append(default)
        self.__init__(tuple(args), currentRotation=rotation)



class PolygonInformationObject(object):
    def __init__(self, verticesNum, radius, color, alphaLimit, alphaShiftDuration, rotationSpeed, rotationIncrementSpeed, alphaOverflowFunc=modAlpha, alphaReverse=False):
        self.args = {
            'verticesNum': verticesNum,
            'radius': radius,
            'color': color,
            'alphaLimit': alphaLimit,
            'alphaShiftDuration': alphaShiftDuration,
            'rotationSpeed': rotationSpeed,
            'rotationIncrementSpeed': rotationIncrementSpeed,
            'alphaOverflowFunc': alphaOverflowFunc,
            'alphaReverse': alphaReverse
        }

        self.verticesNum = verticesNum
        self.radius = radius
        self.color = color
        self.alphaLimit = alphaLimit
        self.alphaShiftDuration = alphaShiftDuration
        self.alphaOverflowFunc = alphaOverflowFunc
        self.start = perf_counter()
        self.alphaReverse = alphaReverse

        self.rotationSpeed = rotationSpeed
        self.rotationIncrementSpeed = rotationIncrementSpeed

        self.alphaDifference = alphaLimit[1] - alphaLimit[0]
        self.alphaDifference = self.alphaDifference if self.alphaDifference else 1
        self.alphaWaveLength = 2*pi/self.alphaDifference
        self.meanInAlphaLimit = (self.alphaLimit[0] + self.alphaLimit[1])/2
        self.alpha = 0

    def giveGFXDrawArgument(self, dt, rotation):
        # what does it need to return... well it needs to return the GFXDrawShapes arg and Max x and y so it can make a surface large enough. simple
        # lets first see what parts of the previous code we need
        # realised it doesn't need x and y
        self.alpha = (perf_counter() - self.start) / \
            self.alphaShiftDuration*self.alphaDifference
        self.IMGAlpha = self.alphaOverflowFunc(
            self.alpha, self.alphaLimit, self.alphaReverse, self.alphaDifference, self.alphaWaveLength, self.meanInAlphaLimit)

        rotation *= self.rotationSpeed
        self.rotationSpeed += self.rotationIncrementSpeed*dt
        return (self.verticesNum, self.radius, self.color, rotation, self.IMGAlpha)

    def giveInitialArgument(self):
        return {
            'verticesNum': self.verticesNum,
            'radius': self.radius,
            'color': self.color,
            'alphaLimit': self.alphaLimit,
            'alphaShiftDuration': self.alphaShiftDuration,
            'rotationSpeed': self.rotationSpeed,
            'rotationIncrementSpeed': self.rotationIncrementSpeed,
            'alphaOverflowFunc': self.alphaOverflowFunc,
            'alphaReverse': self.alphaReverse
        }

# class PolygonInformationObject(object):
#     def __init__(self, verticesNum, radius, color, alphaLimit, alphaShiftDuration, rotation, rotationIncrement, alphaOverflowFunc=modAlpha, alphaReverse=False):
#         self.args = {
#             'verticesNum': verticesNum,
#             'radius': radius,
#             'color': color,
#             'alphaLimit': alphaLimit,
#             'alphaShiftDuration': alphaShiftDuration,
#             'rotation': rotation,
#             'rotationIncrement': rotationIncrement,
#             'alphaOverflowFunc': alphaOverflowFunc,
#             'alphaReverse': alphaReverse
#         }

#         self.verticesNum = verticesNum
#         self.radius = radius
#         self.color = color
#         self.alphaLimit = alphaLimit
#         self.alphaShiftDuration = alphaShiftDuration
#         self.alphaOverflowFunc = alphaOverflowFunc
#         self.start = perf_counter()
#         self.alphaReverse = alphaReverse

#         self.rotation = rotation
#         self.rotationIncrement = rotationIncrement

#         # args dependant and need updating
#         self.alphaDifference = alphaLimit[1] - alphaLimit[0]
#         self.alphaDifference = self.alphaDifference if self.alphaDifference else 1
#         self.alphaWaveLength = 2*pi/self.alphaDifference
#         self.meanInAlphaLimit = (self.alphaLimit[0] + self.alphaLimit[1])/2

#         self.alpha = 0
#         self.IMGAlpha = self.alphaOverflowFunc(
#             self.alpha, self.alphaLimit, self.alphaReverse, self.alphaDifference, self.alphaWaveLength, self.meanInAlphaLimit)

#         self.image = GFXDrawShape(
#             self.verticesNum, self.radius, self.color, self.rotation, self.IMGAlpha)

#     def update(self, dt, externalRotationInc=0, externalRotation=0):
#         self.alpha = (perf_counter() - self.start) / \
#             self.alphaShiftDuration*self.alphaDifference
#         self.IMGAlpha = self.alphaOverflowFunc(
#             self.alpha, self.alphaLimit, self.alphaReverse, self.alphaDifference, self.alphaWaveLength, self.meanInAlphaLimit)

#         self.rotation += (self.rotationIncrement+externalRotationInc)*dt
#         self.image = GFXDrawShape(
#             self.verticesNum, self.radius, self.color, externalRotation+self.rotation, self.IMGAlpha)

#     def copy(self):
#         # need to make a copy which doesn't redirect to the same class object
#         return PolygonInformationObject(self.verticesNum, self.radius, self.color, self.alphaLimit, self.alphaShiftDuration, self.rotation, self.rotationIncrement, self.alphaOverflowFunc, self.alphaReverse)

#     def copyAndEdit(self, dictOfAttribute):

#         args = {
#             'verticesNum': self.verticesNum,
#             'radius': self.radius,
#             'color': self.color,
#             'alphaLimit': self.alphaLimit,
#             'alphaShiftDuration': self.alphaShiftDuration,
#             'rotation': self.rotation,
#             'rotationIncrement': self.rotationIncrement,
#             'alphaOverflowFunc': self.alphaOverflowFunc,
#             'alphaReverse': self.alphaReverse}

#         for key, item in dictOfAttribute.items():
#             # setattr(object, key, item)
#             args[key] = item
#         return PolygonInformationObject(*args.values())

#     def edit(self, argsAsDict):
#         for key, item in argsAsDict.items():
#             self.args[key] = item
#         self.__init__(**self.args)

#     def returnGFXargs(self):
#         return (self.verticesNum, self.radius, self.color, self.rotation, self.IMGAlpha)


class TrailOverviewObject(object):
    # remember to change args if changing arg here
    def __init__(self, trailObject, timerDuration, spawnTimer, target, changesToPolygon):
        self.args = {
            'trailObject': trailObject,
            'timerDuration': timerDuration,
            'spawnTimer': spawnTimer,
            'target': target,
            'changesToPolygon': changesToPolygon
        }

        self.timerDuration = timerDuration  # timerDuration is how long the bullet
        self.spawnTimer = spawnTimer
        self.spawnStart = perf_counter()
        self.trailObject = trailObject
        self.target = target  # target is what we get the copy of

        # This eval is redundant but keeping it if I come across value which is changing

        #expression = "{'rotationIncrement' : target.movementAngle, 'alphaLimit' : (0, 255), 'alphaShiftDuration' : 1, 'alphaOverFlowFunc' : sinAlpha}"
        #self.changesUpdate = eval('lambda target: ' + expression)

        self.changesToPolygon = changesToPolygon

    def update(self, TRAILS, ExternalChange=0):

        if TimeIt(self.timerDuration, self.spawnStart) and self.target.isMovement:
            self.spawnStart = perf_counter()

            #self.changes = self.changesUpdate(self.target)

            # self.changeObject.update()

            TRAILS.append(self.trailObject(
                'foo',
                point=PointObject(self.target.position[:], 0, 0),
                polygon=self.target.polygon.returnSelfAndEdit(self.changesToPolygon, self.target.polygon.rotation),
                killTimer=self.spawnTimer))
            # self.trailObject()

    def edit(self, argsAsDict):
        for key, item in argsAsDict.items():
            self.args[key] = item
        self.__init__(**self.args)


# class TrailInformationObject(object):
#     # remember to change args if changing arg here
#     def __init__(self, trailObject, timerDuration, spawnTimer, target, changesToPolygon):
#         self.args = {
#             'trailObject': trailObject,
#             'timerDuration': timerDuration,
#             'spawnTimer': spawnTimer,
#             'target': target,
#             'changesToPolygon': changesToPolygon
#         }

#         self.timerDuration = timerDuration  # timerDuration is how long the bullet
#         self.spawnTimer = spawnTimer
#         self.spawnStart = perf_counter()
#         self.trailObject = trailObject
#         self.target = target  # target is what we get the copy of

#         # This eval is redundant but keeping it if I come across value which is changing

#         #expression = "{'rotationIncrement' : target.movementAngle, 'alphaLimit' : (0, 255), 'alphaShiftDuration' : 1, 'alphaOverFlowFunc' : sinAlpha}"
#         #self.changesUpdate = eval('lambda target: ' + expression)

#         self.changesToPolygon = changesToPolygon

#     def update(self, TRAILS, ExternalChange=0):

#         if TimeIt(self.timerDuration, self.spawnStart) and self.target.isMovement:
#             self.spawnStart = perf_counter()

#             #self.changes = self.changesUpdate(self.target)

#             # self.changeObject.update()

#             TRAILS.append(self.trailObject('foo', point=PointObject(
#                 self.target.position[:], 0, 0), polygon=self.target.polygon.copyAndEdit(self.changesToPolygon), killTimer=self.spawnTimer))
#             # self.trailObject()

#     def edit(self, argsAsDict):
#         for key, item in argsAsDict.items():
#             self.args[key] = item
#         self.__init__(**self.args)


# Brain Thinking Spot

# how does it get het polygon info.
# either it's has a target to copy from or a template which it want's to copy. we want the person to in theory choose. What i may have to do is Instruction manual.

# how to make the instruction manual.
# I don't want to use eval cause bad code practice and it is the easiest way to do it.
# what I need is a class that can hold changing values and have a way to change stuff.

# what i know
# I need target which is the target (who could have thought) which has some changing data
# some data want to be utilised such as angleIncrement.
# so if
# wait get attribute
# if someone want to use angleIncrement we send a signal saying angleIncrement will be used. now when we get a

# in the end it uses dict...
