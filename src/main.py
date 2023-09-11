import game
import maze
import pacman
import ghost
import pygame 
import sys
import mainMenu
import sound
from pygame.locals import *
import os 
import path

def CheckIfCloseButton(events):
    for event in events:
        if event.type == QUIT:
            sys.exit(0)

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

    window = pygame.display.set_mode(thisGame.screenSize)
                
    thisGame.DrawMap(thisLevel, screen, pygame.time.get_ticks(), ghosts, thisGame, thisPath, thisPacman)
    for i in range(0, 4, 1):
        ghosts[i].Move(thisPath, thisPacman, thisGame, thisLevel)
        ghosts[i].Draw(thisGame, thisPacman, screen, ghosts)
    thisPacman.Draw(screen, thisGame)  
    thisGame.StartNewGame(thisPath, thisLevel, thisPacman, ghosts)

    ########### GAME LOOP ###########
    while True:
        CheckIfCloseButton(pygame.event.get())
        screen.fill((0, 0, 0))  # Fill the screen with black
        thisGame.ChangeDirection(thisPacman, thisLevel, thisPath, ghosts)
        thisGame.DrawMap(thisLevel, screen, pygame.time.get_ticks(), ghosts, thisGame, thisPath, thisPacman)
        thisGame.DrawLifes(screen)

        if thisGame.mode == 1:
            thisPacman.Move(thisLevel, thisGame, ghosts, thisPath, screen)
            for i in range(0, 4, 1):
                ghosts[i].Move(thisPath, thisPacman, thisGame, thisLevel)
                ghosts[i].Draw(thisGame, thisPacman, screen, ghosts)  

            thisPacman.Draw(screen, thisGame)
            thisGame.DrawScore(screen, thisGame)
        
        pygame.display.update()
        clock.tick(60)
