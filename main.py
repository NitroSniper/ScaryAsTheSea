from engine import TimeIt
import pygame
from statistics import mean
from time import perf_counter as perf_counter
from Player import PlayerObject
from Bullets import SimpleBullet, Bullets
from random import randint
from Composition import GameListPointers, sinAlpha, modAlpha, maxAlpha
from pygame.locals import (
    QUIT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    K_w,
    K_s,
    K_a,
    K_d,
    K_SPACE,
    K_UP,
    K_DOWN,
    K_RIGHT,
    K_LEFT,
    # K_j,
    # K_k,
    # K_l,
    # K_i
)





SCREEN_WIDTH = 1920*1
SCREEN_HEIGHT = 1080*1
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_SIZE = (1080, 540)  # x, y
# WINDOW_SIZE = (1920, 1080)
pygame.display.set_caption("Template")
# Set the Caption Window Like 'Terraria: Also Try Minecraft'
DISPLAY = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # True Screen
# Screen to Blit on other Screen
SCREEN = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

P2 = PlayerObject((K_UP, K_DOWN, K_LEFT, K_RIGHT), K_SPACE, 4, (400, 200))
P1 = PlayerObject((K_w, K_s, K_a, K_d), K_SPACE, 4, (0, 0))


# {
#             'verticesNum' : vertices,
#             'radius' : 20,
#             'color' : (3, 207, 252),
#             'alphaLimit' : (255, 255),
#             'alphaShiftDuration' : 1,
#             'rotation' : 0,
#             'rotationIncrement' : 1}

changes = ({
    'color': (110, 1, 95),
    'verticesNum': 5

},)

P1.polygon.editSelf(changes)

# {
#             'trailObject' : MotionBlurTrail,
#             'timerDuration' : 0.05,
#             'spawnTimer' : 1,
#             'target' : self
#         }

polychange = ({
    'alphaLimit': (0, 150),
    'alphaShiftDuration': 0.5,
    'alphaOverflowFunc': sinAlpha

},)
changes = {
    'timerDuration': 0.01,
    'spawnTimer': 1,
    'changesToPolygon': polychange
}


P1.trail.edit(changes)


# P2.customize({
#     'angleIncrement' : 0,
#     'angleIncrementMoving' : 0,
#     'color' : (3, 207, 252),
#     'trailDuration' : 2,
#     'trailTimer' : 0.1,
#     'MinorChanges' : (0, 200, True),
#     'alphaChangeDuration' : (2, modAlpha),
#     'numSides' : 3

# })

SCREENTODISPLAYSCALAR = tuple(
    win/scr for win, scr in zip(WINDOW_SIZE, SCREEN_SIZE))

PLAYERLOOPORDER = ((KEYDOWN, True), (KEYUP, False))
frame = []
displayframe = []

l1, l2, l3, l4 = [], [], [], []

HDMode = True


def DrawImages():
    pass


def Game():
    SCREEN.fill((14, 18, 36))
    DISPLAY.blit(pygame.transform.scale(SCREEN, WINDOW_SIZE), (0, 0))
    pygame.display.update()

    start = perf_counter()
    PLAYERS = [P1, P2]
    GameListPointers.PLAYERS = PLAYERS
    TRAILS = GameListPointers.TRAILS
    BULLETS = GameListPointers.BULLETS

    # BULLETS.append(SimpleBullet(
    #     120, 'triangleWithCore', (700, 100), 0, 0, 1, 1))
    # BULLETS.append(SimpleBullet(
    #     120, 'triangleWithCore', (820, 340), 0, 0, 1, 1))
    # BULLETS.append(SimpleBullet(
    #     30, 'triangleWithCore', (940, 100), 0, 0, 1, 1))
    for n in range(10):
        SimpleBullet(10, (120*n, 670), 0, 240, 'triangleWithCore')
    screenOffset = [0,0]
    programRunning = True
    shake = perf_counter()
    while programRunning:
        dt = (perf_counter() - start)*120
        start = perf_counter()
        lstart = perf_counter()

        for event in pygame.event.get():
            for keyState, value in PLAYERLOOPORDER:
                if event.type == keyState:
                    for player in PLAYERS:
                        for controlKey, direction in zip(player.moveSet, player.movement):
                            if event.key == controlKey:
                                player.movement[direction] = value
            if event.type == QUIT:
                programRunning = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                programRunning = False

        l1.append(1/(perf_counter()-lstart))
        lstart = perf_counter()

        # Game Update
        for player in PLAYERS:
            player.update(dt)
        for trail in TRAILS:
            trail.update(dt)
        for bullet in BULLETS:
            bullet.update(dt)


        #Recode this better!!!!!!!
        if screenOffset != [0,0]:
            if screenOffset[0] > 0:
                if screenOffset[0] < 1:
                    screenOffset[0] = 0
                else:
                    screenOffset[0] -= 1*dt
            elif screenOffset[0] < 0:
                if screenOffset[0] > -1:
                    screenOffset[0] = 0
                else:
                    screenOffset[0] += 1*dt
            if screenOffset[1] > 0:
                if screenOffset[1] < 1:
                    screenOffset[1] = 0
                else:
                    screenOffset[1] -= 1*dt
            elif screenOffset[1] < 0:
                if screenOffset[1] > -1:
                    screenOffset[1] = 0
                else:
                    screenOffset[1] += 1*dt

        if TimeIt(0.5, shake):
            shake = perf_counter()
            #screenOffset = [0, 10]


        l2.append(1/(perf_counter()-lstart))
        lstart = perf_counter()

        # Drawing
        SCREENRECT = []
        SCREEN.fill((14, 18, 36))

        for trail in TRAILS:
            SCREENRECT.append(SCREEN.blit(trail.image, trail.position))

        for bullet in BULLETS:
            SCREENRECT.append(SCREEN.blit(bullet.image, bullet.position))
        
        for player in PLAYERS:
            SCREENRECT.append(SCREEN.blit(player.image, player.position))


        l3.append(1/(perf_counter()-lstart))
        lstart = perf_counter()

        # alist = []
        # for rect in SCREENRECT:
        #     alist.append((rect[0]*SCREENTODISPLAYSCALAR[0],
        #                   rect[1]*SCREENTODISPLAYSCALAR[1],
        #                   rect[2]*SCREENTODISPLAYSCALAR[0]+1,
        #                   rect[3]*SCREENTODISPLAYSCALAR[1]+1))

        # SCREEN.blit(GFXDrawShapes([(3, 160, (255, 255, 255), angle, 255)]), (400,400))
        #SCREEN.blit(GFXDrawShapes([(3, 40, (255, 255, 255), 0, 255), (3, 20, (0, 0 ,0 ), 0, 0)]), (600,400))

        if not HDMode:
            DISPLAY.blit(pygame.transform.scale(SCREEN, WINDOW_SIZE), screenOffset)
        else:
            DISPLAY.blit(pygame.transform.smoothscale(
                SCREEN, WINDOW_SIZE), screenOffset)
        pygame.display.update()
        l4.append(1/(perf_counter()-lstart))
        displayframe.append(1/(perf_counter()-start))

    print(f'''
               Event Handler: {mean(l1)}
               Update Handler: {mean(l2)}
               Drawing Handler: {mean(l3)}
               Display Handler: {mean(l4)}
               Total Frame: {mean(displayframe)}
               Total Trail: {len(TRAILS)}
               ''')


if __name__ == '__main__':
    Game()
    pygame.quit()
