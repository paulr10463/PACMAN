
SCREEN_TILE_SIZE_HEIGHT = 23
SCREEN_TILE_SIZE_WIDTH = 30
TILE_WIDTH = 15
TILE_HEIGHT = 23

class game:

    def __init__(self):
        self.lives = 3
        self.screenTileSize = (SCREEN_TILE_SIZE_HEIGHT, SCREEN_TILE_SIZE_WIDTH)
        self.screenSize = (self.screenTileSize[1] * TILE_WIDTH, self.screenTileSize[0] * TILE_HEIGHT)
        self.screenPixelOffset = (0, 0)  # offset in pixels of the screen from its nearest-tile position

    def StartNewGame(self):
        self.score = 0
        self.lives = 3


