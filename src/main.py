import game
import maze
import pygame 
import sys
import os
from pygame.locals import *


# Joystick defaults - maybe add a Preferences dialog in the future?
JS_DEVNUM = 0  # device 0 (pygame joysticks always start at 0). if JS_DEVNUM is not a valid device, will use 0


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

while True:
    CheckIfCloseButton(pygame.event.get())
    thisGame.DrawMap(thisLevel, screen)
    pygame.display.update()








    

