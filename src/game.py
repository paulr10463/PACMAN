
import utils
import os
import pygame
import sys

ASSETS_PATH = os.getcwd()+"/res/text/"
LAP_TIME = 10000
if os.name == "nt":
    SCRIPT_PATH = os.getcwd()

SCREEN_TILE_SIZE_HEIGHT = 24
SCREEN_TILE_SIZE_WIDTH = 20
TILE_WIDTH = TILE_HEIGHT = 24

# new constants for the score's position
SCORE_XOFFSET = 50  # pixels from left edge
SCORE_YOFFSET = 34  # pixels from bottom edge (to top of score)
rect_list = []  # rect list for drawing


tileIDName = {}  # gives tile name (when the ID# is known)
tileID = {}  # gives tile ID (when the name is known)
tileIDImage = {}  # gives tile image (when the ID# is known)


class game:
    def __init__(self):
        self.lives = 3
        self.mode = 1
        self.screenTileSize = (SCREEN_TILE_SIZE_HEIGHT, SCREEN_TILE_SIZE_WIDTH)
        self.screenSize = (self.screenTileSize[1] * TILE_WIDTH, self.screenTileSize[0] * TILE_HEIGHT)
        self.screenPixelOffset = (0, 0)  # offset in pixels of the screen from its nearest-tile position
        self.score = 0
        self.imLife = utils.get_image_surface(os.path.join(SCRIPT_PATH, "res", "text", "life.gif"))
        self.fruit = -1
        self.fruitEaten = False
        self.fruitLap = 0
        self.fruitTiles = {}

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
        self.fruitTiles = [tileID['fruit-0'], tileID['fruit-1'], tileID['fruit-2'], tileID['fruit-3'], tileID['fruit-4']]
        #print(fruitTiles)    

    def DrawMap(self, level, screen, time):
        self.GetCrossRef()
        lap = (time//LAP_TIME) % 5   #each 10 sec is a lap
        if self.fruitLap != lap:
            self.fruitEaten = False
        time = time % LAP_TIME #the max time will be 10 secs
        self.fruitLap = lap

        for row in range(-1, self.screenTileSize[0] + 1):
            for col in range(-1, self.screenTileSize[1] + 1):
                actualRow = row
                actualCol = col
                useTile = level.GetMapTile((actualRow, actualCol))

                if (row == 12 and col == 9):
                    if (time > LAP_TIME*0.1 and time < LAP_TIME*0.8) and (self.fruitEaten == False) :    
                        self.setNewFruit(level,lap+5)
                        screen.blit(tileIDImage[self.fruit], (col * TILE_WIDTH , row * TILE_HEIGHT))                   
    

                elif useTile != 0 and useTile != tileID['door-h'] and useTile != tileID['door-v']:
                    # if this isn't a blank tile
                    screen.blit(tileIDImage[useTile], (col * TILE_WIDTH ,
                                                           row * TILE_HEIGHT))

    #LifeCounter 
    def DrawLifes(self,screen):
        for i in range(0, self.lives, 1):
            life_image = pygame.transform.scale(self.imLife, (20, 20))
            screen.blit(life_image, (34 + i * 20 + 16, self.screenSize[1] - 30))

    
    
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

    def AddToScore(self, amount):
        self.score += amount  
        print("Score: " + str(self.score))   

    def GetFruitTiles(self):
        return self.fruitTiles

    def setFruitEaten(self, level):
        self.AddToScore(100)
        level.SetMapTile((12, 9), 0)
        self.fruit = -1
        self.fruitEaten = True
        self.AddToScore(100)

    def setNewFruit(self, level, fruit):
        level.SetMapTile((12, 9), fruit)
        self.fruit = fruit
        self.fruitEaten = False

