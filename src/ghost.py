import utils
import os
import random
import math

if os.name == "nt":
    SCRIPT_PATH = os.getcwd()
    
TILE_WIDTH = TILE_HEIGHT = 24

ghostcolor = {
    0: (255, 0, 0, 255),
    1: (255, 128, 255, 255),
    2: (128, 255, 255, 255),
    3: (255, 128, 0, 255),
    4: (50, 50, 255, 255),
    5: (255, 255, 255, 255)}

class ghost:
    def __init__(self, ghostID):
        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.speed = 1.5

        self.nearestRow = 0
        self.nearestCol = 0

        self.id = ghostID
        if self.id == 0:
            self.x = 10 * TILE_WIDTH
            self.y = 10 * TILE_HEIGHT
        elif self.id == 1:
            self.x = 9 * TILE_WIDTH
            self.y = 10 * TILE_HEIGHT
        elif self.id == 2:
            self.x = 8 * TILE_WIDTH
            self.y = 10 * TILE_HEIGHT
        elif self.id == 3:
            self.x = 9 * TILE_WIDTH
            self.y = 8 * TILE_HEIGHT

        # ghost "state" variable
        # 1 = normal
        # 2 = vulnerable
        # 3 = spectacles
        self.state = 1

        self.homeX = 10 * TILE_HEIGHT
        self.homeY = 10 * TILE_WIDTH

        self.currentPath = ""

        self.anim = {}
        for i in range(1, 7, 1):
            self.anim[i] = utils.get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "ghost " + str(i) + ".gif"))

            # change the ghost color in this frame
            for y in range(0, TILE_HEIGHT, 1):
                for x in range(0, TILE_WIDTH, 1):

                    if self.anim[i].get_at((x, y)) == (255, 0, 0, 255):
                        # default, red ghost body color
                        self.anim[i].set_at((x, y), ghostcolor[self.id])

        self.animFrame = 1
        self.animDelay = 0

    def RestartGhost(self, level, thisGame, path, thisPacman):
        if self.id == 0:
            self.x = 10 * TILE_WIDTH
            self.y = 10 * TILE_HEIGHT
        elif self.id == 1:
            self.x = 9 * TILE_WIDTH
            self.y = 10 * TILE_HEIGHT
        elif self.id == 2:
            self.x = 8 * TILE_WIDTH
            self.y = 10 * TILE_HEIGHT
        elif self.id == 3:
            self.x = 9 * TILE_WIDTH
            self.y = 8 * TILE_HEIGHT
            
        self.velX = 0
        self.velY = 0
        self.state = 1
        self.speed = 1.5
        self.Move(path, thisPacman, thisGame, level)

        # give each ghost a path to a random spot (containing a pellet)
        (randRow, randCol) = (0, 0)

        while not level.GetMapTile((randRow, randCol)) == thisGame.GetTileID().get('pellet') or (randRow, randCol) == (10 * TILE_HEIGHT, 10 * TILE_WIDTH):
            randRow = random.randint(1, level.lvlHeight - 2)
            randCol = random.randint(1, level.lvlWidth - 2)

        # print "Ghost " + str(i) + " headed towards " + str((randRow, randCol))
        self.currentPath = path.FindPath((self.nearestRow, self.nearestCol), (randRow, randCol))
        self.FollowNextPathWay(path, thisPacman, level, thisGame) 

    def Draw(self, thisGame, player, screen, ghosts):
        global rect_list
        pupilSet = None

        if thisGame.mode == 3:
            return False

        # ghost eyes --
        for y in range(6, 12, 1):
            for x in [5, 6, 8, 9]:
                self.anim[self.animFrame].set_at((x, y), (248, 248, 248, 255))
                self.anim[self.animFrame].set_at((x + 9, y), (248, 248, 248, 255))

                if player.x > self.x and player.y > self.y:
                    # player is to lower-right
                    pupilSet = (8, 9)
                elif player.x < self.x and player.y > self.y:
                    # player is to lower-left
                    pupilSet = (5, 9)
                elif player.x > self.x and player.y < self.y:
                    # player is to upper-right
                    pupilSet = (8, 6)
                elif player.x < self.x and player.y < self.y:
                    # player is to upper-left
                    pupilSet = (5, 6)
                else:
                    pupilSet = (5, 9)

        for y in range(pupilSet[1], pupilSet[1] + 3, 1):
            for x in range(pupilSet[0], pupilSet[0] + 2, 1):
                self.anim[self.animFrame].set_at((x, y), (0, 0, 255, 255))
                self.anim[self.animFrame].set_at((x + 9, y), (0, 0, 255, 255))
        # -- end ghost eyes

        if self.state == 1:
            # draw regular ghost (this one)
            screen.blit(self.anim[self.animFrame],
                        (self.x - thisGame.screenPixelOffset[0], self.y - thisGame.screenPixelOffset[1]))
        elif self.state == 2:
            # draw vulnerable ghost

            if thisGame.ghostTimer > 100:
                # blue
                screen.blit(ghosts[4].anim[self.animFrame],
                            (self.x - thisGame.screenPixelOffset[0], self.y - thisGame.screenPixelOffset[1]))
            else:
                # blue/white flashing
                tempTimerI = int(thisGame.ghostTimer / 10)
                if tempTimerI == 1 or tempTimerI == 3 or tempTimerI == 5 or tempTimerI == 7 or tempTimerI == 9:
                    screen.blit(ghosts[5].anim[self.animFrame],
                                (self.x - thisGame.screenPixelOffset[0], self.y - thisGame.screenPixelOffset[1]))
                else:
                    screen.blit(ghosts[4].anim[self.animFrame],
                                (self.x - thisGame.screenPixelOffset[0], self.y - thisGame.screenPixelOffset[1]))

        elif self.state == 3:
            # draw glasses
            screen.blit(thisGame.GetTileIDImage().get(thisGame.GetTileID().get('glasses')),
                        (self.x - thisGame.screenPixelOffset[0], self.y - thisGame.screenPixelOffset[1]))

        if thisGame.mode == 6 or thisGame.mode == 7:
            # don't animate ghost if the level is complete
            return False

        self.animDelay += 1

        if self.animDelay == 2:
            self.animFrame += 1

            if self.animFrame == 7:
                # wrap to beginning
                self.animFrame = 1

            self.animDelay = 0

    def UpdateSpeed(self, player):
        # Aumenta la velocidad en función de los puntos obtenidos por Pac-Man
        self.speed = 2 + (player.points // 100)

    def Move(self, path, player, thisGame, thisLevel):
        self.x += self.velX
        self.y += self.velY

        self.nearestRow = int(((self.y + (TILE_HEIGHT / 2)) / TILE_HEIGHT))
        self.nearestCol = int(((self.x + (TILE_HEIGHT / 2)) / TILE_WIDTH))

        if (self.x % TILE_WIDTH) == 0 and (self.y % TILE_HEIGHT) == 0:
            # if the ghost is lined up with the grid again
            # meaning, it's time to go to the next path item

            if self.currentPath is not False and (len(self.currentPath) > 0):
                self.currentPath = self.currentPath[1:]
                self.FollowNextPathWay(path, player, thisLevel, thisGame)

            else:
                self.x = self.nearestCol * TILE_WIDTH
                self.y = self.nearestRow * TILE_HEIGHT

                # chase pac-man
                self.currentPath = path.FindPath((self.nearestRow, self.nearestCol),
                                                 (player.nearestRow, player.nearestCol))
                self.FollowNextPathWay(path, player, thisLevel, thisGame)
                
    def FollowNextPathWay(self, path, player, thisLevel, thisGame):
        # print "Ghost " + str(self.id) + " rem: " + self.currentPath
        # only follow this pathway if there is a possible path found!
        if not self.currentPath == False:

            if len(self.currentPath) > 0:
                if self.currentPath[0] == "L":
                    (self.velX, self.velY) = (-self.speed, 0)
                elif self.currentPath[0] == "R":
                    (self.velX, self.velY) = (self.speed, 0)
                elif self.currentPath[0] == "U":
                    (self.velX, self.velY) = (0, -self.speed)
                elif self.currentPath[0] == "D":
                    (self.velX, self.velY) = (0, self.speed)

            else:
                # this ghost has reached his destination!!
                if not self.state == 3:
                    # chase pac-man
                    self.currentPath = path.FindPath((self.nearestRow, self.nearestCol),
                                                     (player.nearestRow, player.nearestCol))
                    self.FollowNextPathWay(path, player, thisLevel, thisGame)

                else:
                    # glasses found way back to ghost box
                    self.state = 1
                    self.speed = self.speed / 4

                    # give ghost a path to a random spot (containing a pellet)
                    (randRow, randCol) = (0, 0)

                    while not thisLevel.GetMapTile((randRow, randCol)) == thisGame.GetTileID().get('pellet') or (randRow, randCol) == (
                            0, 0):
                        randRow = random.randint(1, thisLevel.lvlHeight - 2)
                        randCol = random.randint(1, thisLevel.lvlWidth - 2)

                    self.currentPath = path.FindPath((self.nearestRow, self.nearestCol), (randRow, randCol))
                    self.FollowNextPathWay(path, player, thisLevel, thisGame)