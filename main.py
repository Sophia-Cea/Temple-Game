import pygame
import sys
from state import *


pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
display = pygame.Surface((WIDTH, HEIGHT))
stateManager = StateManager()

stateManager.push(PlayState())

running = True
while running:
    delta = fpsClock.tick(60)/1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    WIDTH, HEIGHT = screen.get_size()
    stateManager.run(display, events)
    screen.blit(pygame.transform.scale(display, (WIDTH, HEIGHT)), (0,0))
    pygame.display.flip()