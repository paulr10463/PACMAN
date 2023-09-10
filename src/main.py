import game
import time
import maze
import pacman
import ghost
import pygame 
import sys
import mainMenu
from pygame.locals import *
import os 
import path
import random

TILE_WIDTH = TILE_HEIGHT = 24

os.environ['SDL_VIDEO_WINDOW_POS'] = 'centered'

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
    thisPath = path.path_finder()
    thisLevel.LoadLevel(thisPath)
    
    # create ghost objects
    ghosts = {}
    for i in range(0, 6, 1):
        # remember, ghost[4] is the blue, vulnerable ghost
        ghosts[i] = ghost.ghost(i)

    # Set the initial position of the red ghost (ghosts[3]) to the middle of the board
    #red_ghost = ghosts[3]
    #red_ghost.nearestRow = thisGame.screenSize[1] // (2 * TILE_HEIGHT)
    #red_ghost.nearestCol = thisGame.screenSize[0] // (2 * TILE_WIDTH)

    #window = pygame.display.set_mode(thisGame.screenSize, pygame.FULLSCREEN)
    window = pygame.display.set_mode(thisGame.screenSize)

    def CheckIfCloseButton(events):
        for event in events:
            if event.type == QUIT:
                sys.exit(0)

    ########### GAME LOOP ###########
    while True:
        CheckIfCloseButton(pygame.event.get())
        screen.fill((0, 0, 0))  # Fill the screen with black

        thisGame.ChangeDirection(thisPacman, thisLevel)
        thisGame.DrawMap(thisLevel, screen, pygame.time.get_ticks(), thisPath)
        thisGame.DrawLifes(screen)
        thisPacman.Move(thisLevel, thisGame, ghosts, thisPath, screen)
        ##ghosts[0].Move(thisPath, thisPacman, thisGame, thisLevel)   
        ##ghosts[2].Move(thisPath, thisPacman, thisGame, thisLevel)  
        
        
        for i in range(0, 4, 1):
            ghosts[i].Move(thisPath, thisPacman, thisGame, thisLevel)

            (randRow, randCol) = (0, 0)
            if pygame.time.get_ticks() < 250:
                if i == 0:  # Rojo
                    randRow = 1  # Esquina superior izquierda
                    randCol = 1
                elif i == 1:  # Rosa
                    randRow = 1  # Mover hacia arriba y luego a la izquierda
                    randCol = thisLevel.lvlWidth - 2
                elif i == 2:  # Rosa
                    randRow = thisLevel.lvlHeight - 3  # Esquina superior derecha
                    randCol = 1
                elif i == 3:  # Celeste
                    randRow = thisLevel.lvlHeight - 3  # Esquina inferior derecha
                    randCol = thisLevel.lvlWidth - 2
                
                ghosts[i].currentPath = thisPath.FindPath((ghosts[i].nearestRow, ghosts[i].nearestCol), (randRow, randCol))
                ghosts[i].FollowNextPathWay(thisPath, thisPacman, thisLevel, thisGame)
                        
        for i in range(0, 4, 1):
            ghosts[i].Draw(thisGame, thisPacman, screen, ghosts)

        thisPacman.Draw(screen, thisGame)
        
        pygame.display.update()
        clock.tick(60)
