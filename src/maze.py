import os
import random

TILE_WIDTH = TILE_HEIGHT = 24
LEVEL_WIDTH = 19
LEVEL_HEIGHT = 23
BGCOLOR = [0, 0, 0]
EDGELIGHTCOLOR = [0, 0, 255]
EDGESHADOWCOLOR = [0, 0, 255]
FILLCOLOR = [0, 0, 0]
PELLETCOLOR = [255, 255, 255]

SCRIPT_PATH = os.getcwd()

class level:
    def __init__(self):
        self.lvlWidth = LEVEL_WIDTH
        self.lvlHeight = LEVEL_HEIGHT
        self.edgeLightColor = EDGELIGHTCOLOR
        self.edgeShadowColor = EDGESHADOWCOLOR
        self.fillColor = FILLCOLOR
        self.map = {}

    def LoadLevel(self, path):      
        f = open(os.path.join(SCRIPT_PATH, "res", "levels", "1_design.txt"), 'r')
        rowNum = 0
        for line in f:
            str_splitBySpace = line.split(' ')
            for k in range(0, self.lvlWidth, 1):
                self.SetMapTile((rowNum, k), int(str_splitBySpace[k]))
            rowNum += 1

        f.close()
        
        # load map into the pathfinder object
        path.ResizeMap((self.lvlHeight, self.lvlWidth))

        for row in range(0, path.size[0], 1):
            for col in range(0, path.size[1], 1):
                if self.IsWall((row, col)):
                    path.SetType((row, col), 1)
                else:
                    path.SetType((row, col), 0)

    def SetMapTile(self, row_col, newValue):
        (row, col) = row_col
        self.map[(row * self.lvlWidth) + col] = newValue

    def GetMapTile(self, row_col):
        (row, col) = row_col
        if 0 <= row < self.lvlHeight and 0 <= col < self.lvlWidth:
            return self.map[(row * self.lvlWidth) + col]
        else:
            return 0
    
    def IsWall(self, row_col):
        (row, col) = row_col
        if row > self.lvlHeight - 1 or row < 0:
            return True

        if col > self.lvlWidth - 1 or col < 0:
            return True

        # check the offending tile ID
        result = self.GetMapTile((row, col))

        # if the tile was a wall
        if 100 <= result <= 199:
            return True
        else:
            return False

    def Restart(self, ghosts, path, player, thisGame):
        # move ghosts back to home
        for i in range(0, 4, 1):
            ghosts[i].RestartGhost(self, thisGame, path, player)
            
        player.x = player.homeX
        player.y = player.homeY
        player.velX = 0
        player.velY = 0

        player.anim_pacmanCurrent = player.anim_pacmanS
        player.animFrame = 3
        
    