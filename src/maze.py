import os

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

    def LoadLevel(self):      
        f = open(os.path.join(SCRIPT_PATH, "res", "levels", "1_design.txt"), 'r')
        rowNum = 0
        for line in f:
            str_splitBySpace = line.split(' ')
            for k in range(0, self.lvlWidth, 1):
                self.SetMapTile((rowNum, k), int(str_splitBySpace[k]))
            rowNum += 1

        f.close()

    def SetMapTile(self, row_col, newValue):
        (row, col) = row_col
        self.map[(row * self.lvlWidth) + col] = newValue

    def GetMapTile(self, row_col):
        (row, col) = row_col
        if 0 <= row < self.lvlHeight and 0 <= col < self.lvlWidth:
            return self.map[(row * self.lvlWidth) + col]
        else:
            return 0
    

    
    



