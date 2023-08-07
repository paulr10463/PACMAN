import game
import maze
import pygame 
import sys
import os
import utils
from pygame.locals import *


# Joystick defaults - maybe add a Preferences dialog in the future?
JS_DEVNUM = 0  # device 0 (pygame joysticks always start at 0). if JS_DEVNUM is not a valid device, will use 0



# Size of tiles
TILE_WIDTH = TILE_HEIGHT = 24

# Must come before pygame.init()
pygame.mixer.pre_init(22050, -16, 1, 1024)
pygame.mixer.init()
pygame.mixer.set_num_channels(7)
channel_backgound = pygame.mixer.Channel(6)

clock = pygame.time.Clock()
pygame.init()

window = pygame.display.set_mode((1, 1))
pygame.display.set_caption("Pacman")

screen = pygame.display.get_surface()
pygame.mouse.set_visible(False)


tileIDName = {}  # gives tile name (when the ID# is known)
tileID = {}  # gives tile ID (when the name is known)
tileIDImage = {}  # gives tile image (when the ID# is known)



if os.name == "nt":
    SCRIPT_PATH = os.getcwd()


# create game and level objects and load first level
thisGame = game.game()
thisLevel = maze.level()
thisLevel.LoadLevel()

#window = pygame.display.set_mode(thisGame.screenSize, pygame.FULLSCREEN)
window = pygame.display.set_mode(thisGame.screenSize)

def CheckIfCloseButton(events):
    for event in events:
        if event.type == QUIT:
            sys.exit(0)

def GetCrossRef():
    crossRefData = utils.readJson("res/crossref.json")
    for element in crossRefData:
            tileIDName[crossRefData[element]] = element
            tileID[element] = crossRefData[element]
            thisID = crossRefData[element]
            tileIDImage[thisID] = utils.get_image_surface(os.path.join(SCRIPT_PATH, "res", "tiles", element + ".gif"))


GetCrossRef()

while True:
    CheckIfCloseButton(pygame.event.get())
    thisLevel.DrawMap(thisGame, screen, tileIDImage, tileID)
        
    pygame.display.update()








    

