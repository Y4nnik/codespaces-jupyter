import pygame
import sys
go = True
screen = pygame.display.set_mode([1200, 550])
while go:
    for event in  pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()