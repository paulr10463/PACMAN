import os
import utils

if os.name == "nt":
    SCRIPT_PATH = os.getcwd()
    
TILE_WIDTH = TILE_HEIGHT = 24

class pacman:
    def __init__(self):
        self.x = 1* TILE_WIDTH
        self.y = 1  * TILE_HEIGHT
        self.velX = 2
        self.velY = 0
        self.speed = 2

        self.nearestRow = 0
        self.nearestCol = 0

        self.homeX = 0
        self.homeY = 0

        self.anim_pacmanL = {}
        self.anim_pacmanR = {}
        self.anim_pacmanU = {}
        self.anim_pacmanD = {}
        self.anim_pacmanS = {}
        self.anim_pacmanCurrent = {}

        self.animFrame = 1

        # Initialize points attribute
        self.points = 0

        for i in range(1, 9, 1):
            self.anim_pacmanL[i] = utils.get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-l " + str(i) + ".gif"))
            self.anim_pacmanR[i] = utils.get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-r " + str(i) + ".gif"))
            self.anim_pacmanU[i] = utils.get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-u " + str(i) + ".gif"))
            self.anim_pacmanD[i] = utils.get_image_surface(
                os.path.join(SCRIPT_PATH, "res", "sprite", "pacman-d " + str(i) + ".gif"))
            self.anim_pacmanS[i] = utils.get_image_surface(os.path.join(SCRIPT_PATH, "res", "sprite", "pacman.gif"))

        self.pelletSndNum = 0

    def Move(self, thisLevel, thisGame):
        self.nearestRow = int(((self.y + (TILE_WIDTH / 2)) / TILE_WIDTH))
        self.nearestCol = int(((self.x + (TILE_HEIGHT / 2)) / TILE_HEIGHT))

        # make sure the current velocity will not cause a collision before moving
        if not self.CheckIfHitWall((self.x + self.velX, self.y + self.velY), (self.nearestRow, self.nearestCol), thisLevel):
            # it's ok to Move
            self.x += self.velX
            self.y += self.velY
            
            # check for collisions with other tiles (pellets, etc)
            self.CheckIfHitSomething((self.x, self.y), (self.nearestRow, self.nearestCol), thisLevel, thisGame)
        else:
            # we're going to hit a wall -- stop moving
            self.velX = 0
            self.velY = 0

    # Add a method to update the points
    def UpdatePoints(self, points):
        self.points += points

    def Draw(self, screen, thisGame):
        # set the current frame array to match the direction pacman is facing
        if self.velX > 0:
            self.anim_pacmanCurrent = self.anim_pacmanR
        elif self.velX < 0:
            self.anim_pacmanCurrent = self.anim_pacmanL
        elif self.velY > 0:
            self.anim_pacmanCurrent = self.anim_pacmanD
        elif self.velY < 0:
            self.anim_pacmanCurrent = self.anim_pacmanU



        screen.blit(self.anim_pacmanCurrent[self.animFrame],
                    (self.x, self.y))

        if thisGame.mode == 1 or thisGame.mode == 8 or thisGame.mode == 9:
            if self.velX != 0 or self.velY != 0:
                # only Move mouth when pacman is moving
                self.animFrame += 1

            if self.animFrame == 9:
                # wrap to beginning
                self.animFrame = 1

    def CheckIfHitWall(self, possiblePlayerX_possiblePlayerY, row_col, thisLevel):
        (possiblePlayerX, possiblePlayerY) = possiblePlayerX_possiblePlayerY
        (row, col) = row_col
        numCollisions = 0

        # check each of the 9 surrounding tiles for a collision
        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):

                if (possiblePlayerX - (iCol * TILE_WIDTH) < TILE_WIDTH) and (
                        possiblePlayerX - (iCol * TILE_WIDTH) > -TILE_WIDTH) and (
                        possiblePlayerY - (iRow * TILE_HEIGHT) < TILE_HEIGHT) and (
                        possiblePlayerY - (iRow * TILE_HEIGHT) > -TILE_HEIGHT):

                    if thisLevel.IsWall((iRow, iCol)):
                        numCollisions += 1

        if numCollisions > 0:
            return True
        else:
            return False
        
    def CheckIfHitSomething(self, playerX_playerY, row_col, thisLevel, thisGame):
        (playerX, playerY) = playerX_playerY
        (row, col) = row_col
        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):

                if (playerX - (iCol * TILE_WIDTH) < TILE_WIDTH) and (
                        playerX - (iCol * TILE_WIDTH) > -TILE_WIDTH) and (
                        playerY - (iRow * TILE_HEIGHT) < TILE_HEIGHT) and (
                        playerY - (iRow * TILE_HEIGHT) > -TILE_HEIGHT):
                    # check the offending tile ID
                    result = thisLevel.GetMapTile((iRow, iCol))

                    if result == thisGame.GetTileID().get('pellet'):
                        # got a pellet
                        thisLevel.SetMapTile((iRow, iCol), 0)
                        thisGame.AddToScore(10)
                        print("Score: " + str(thisGame.score))
                    
                    elif result == thisGame.GetTileID().get('pellet-power'):
                        # got a super-pellet
                        thisLevel.SetMapTile((iRow, iCol), 0)
                        thisGame.AddToScore(50)
                        print("Score: " + str(thisGame.score))

                    elif result == thisGame.GetTileID().get('door-h'):
                        # ran into a horizontal door
                        for i in range(0, thisLevel.lvlWidth, 1):
                            if not i == iCol:
                                if thisLevel.GetMapTile((iRow, i)) == thisGame.GetTileID().get('door-h'):
                                    self.x = i * TILE_WIDTH

                                    if self.velX > 0:
                                        self.x += TILE_WIDTH
                                    else:
                                        self.x -= TILE_WIDTH

                    elif result == thisGame.GetTileID().get('door-v'):
                        # ran into a vertical door
                        for i in range(0, thisLevel.lvlHeight, 1):
                            if not i == iRow:
                                if thisLevel.GetMapTile((i, iCol)) == thisGame.GetTileID().get('door-h'):
                                    self.y = i * TILE_HEIGHT

                                    if self.velY > 0:
                                        self.y += TILE_HEIGHT
                                    else:
                                        self.y -= TILE_HEIGHT