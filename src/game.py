
import utils
import os
import pygame
import sys

if os.name == "nt":
    SCRIPT_PATH = os.getcwd()

SCREEN_TILE_SIZE_HEIGHT = 24
SCREEN_TILE_SIZE_WIDTH = 20
TILE_WIDTH = TILE_HEIGHT = 24


tileIDName = {}  # gives tile name (when the ID# is known)
tileID = {}  # gives tile ID (when the name is known)
tileIDImage = {}  # gives tile image (when the ID# is known)

class game:
    def __init__(self):
        self.lives = 3
        self.mode = 1
        self.screenPixelPos = (0, 0)  # absolute x,y position of the screen from the upper-left corner of the level
        self.screenTileSize = (SCREEN_TILE_SIZE_HEIGHT, SCREEN_TILE_SIZE_WIDTH)
        self.screenSize = (self.screenTileSize[1] * TILE_WIDTH, self.screenTileSize[0] * TILE_HEIGHT)
        self.screenPixelOffset = (0, 0)  # offset in pixels of the screen from its nearest-tile position

    def StartNewGame(self):
        self.score = 0
        self.lives = 3
    
    def GetCrossRef(self):
        crossRefData = utils.readJson("res/crossref.json")
        for element in crossRefData:
                tileIDName[crossRefData[element]] = element
                tileID[element] = crossRefData[element]
                thisID = crossRefData[element]
                tileIDImage[thisID] = utils.get_image_surface(os.path.join(SCRIPT_PATH, "res", "tiles", element + ".gif"))

    def DrawMap(self, level, screen):
        self.GetCrossRef()
        for row in range(-1, self.screenTileSize[0] + 1):
            for col in range(-1, self.screenTileSize[1] + 1):
                actualRow = row
                actualCol = col
                useTile = level.GetMapTile((actualRow, actualCol))
                if useTile != 0 and useTile != tileID['door-h'] and useTile != tileID['door-v']:
                    # if this isn't a blank tile
                    screen.blit(tileIDImage[useTile], (col * TILE_WIDTH ,
                                                           row * TILE_HEIGHT))
                    
    def ChangeDirection(self, player, thisLevel):
        if self.mode == 1 or self.mode == 8 or self.mode == 9:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if not (player.velX == player.speed and player.velY == 0) and not player.CheckIfHitWall(
                        (player.x + player.speed, player.y), (player.nearestRow, player.nearestCol), thisLevel):
                    player.velX = player.speed
                    player.velY = 0

            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                if not (player.velX == -player.speed and player.velY == 0) and not player.CheckIfHitWall(
                        (player.x - player.speed, player.y), (player.nearestRow, player.nearestCol), thisLevel):
                    player.velX = -player.speed
                    player.velY = 0

            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                if not (player.velX == 0 and player.velY == player.speed) and not player.CheckIfHitWall(
                        (player.x, player.y + player.speed), (player.nearestRow, player.nearestCol), thisLevel):
                    player.velX = 0
                    player.velY = player.speed

            elif pygame.key.get_pressed()[pygame.K_UP]:
                if not (player.velX == 0 and player.velY == -player.speed) and not player.CheckIfHitWall(
                        (player.x, player.y - player.speed), (player.nearestRow, player.nearestCol), thisLevel):
                    player.velX = 0
                    player.velY = -player.speed

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit(0)

        elif self.mode == 3:
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                self.StartNewGame()
                
    def GetTileID(self):
        return tileID     
    
    def GetTileIDImage(self):
        return tileIDImage           



