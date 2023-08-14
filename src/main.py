import game
import maze
import pacman
import pygame 
import sys
import mainMenu
from pygame.locals import *
import os 

os.environ['SDL_VIDEO_WINDOW_POS'] = '800,350'

mainMenu = mainMenu.MainMenu()
option = mainMenu.show()

if option == 0:
    pygame.init()
    clock = pygame.time.Clock()
    pygame.init()

    window = pygame.display.set_mode((1, 1))
    pygame.display.set_caption("Pacman")

    screen = pygame.display.get_surface()
    pygame.mouse.set_visible(False)


    # create game and level objects and load first level
    thisGame = game.game()
    thisLevel = maze.level()
    thisPacman = pacman.pacman()
    thisLevel.LoadLevel()

    #window = pygame.display.set_mode(thisGame.screenSize, pygame.FULLSCREEN)
    window = pygame.display.set_mode(thisGame.screenSize)

    def CheckIfCloseButton(events):
        for event in events:
            if event.type == QUIT:
                sys.exit(0)

    while True:
        CheckIfCloseButton(pygame.event.get())
        screen.fill((0, 0, 0))  # Fill the screen with black
        thisGame.ChangeDirection(thisPacman, thisLevel)
        thisGame.DrawMap(thisLevel, screen)
        thisGame.DrawLifes(screen)
        thisPacman.Move(thisLevel, thisGame)
        thisPacman.Draw(screen, thisGame)

        pygame.display.update()
        clock.tick(60)
