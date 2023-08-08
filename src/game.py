
import utils
import os

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

