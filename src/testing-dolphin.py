from minigame.dolphin import DolphinGame
import pygame
width = 1000
height = 500
display = pygame.display.set_mode((width, height)) # dimensions of the window
pygame.init()
game = DolphinGame(display)
game.run()