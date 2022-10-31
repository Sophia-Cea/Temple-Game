import pygame
import sys
from state import *

# TODO next:
# make camera stop at the edges of walls
# make level editor usable again
# design a decent map to use for now

# how should the player be able to control where they shoot?
#   arrow keys
# should the player be free to move all over the screen (including diagonals) or only up/down left/right?
#   yes, all over the screen
# how does player heal?
#   eats the bodies of its enemies.

'''
    TODO
    - make player controller
        - How do you control what direction the bullet shoots?
            - arrow keys
    - rework camera
        - distinguish rooms from each other using doors 
        - only render current room
            - maybe have weird little sparkly thingies like fireflies that exist outside the bounds of the room
    - rework map and rooms so instead of 1 big map you make a bunch of little rooms? 
        - or find a way to use the doors to figure out which room is which by finding closed shapes
    - enemies
        - make moving enemies
        - improve behavior
    - attacks
    - player ability to heal
            - how do you heal??
                - eat the bodies of your enemies..?
    - enemy health and damage
    - inventory
        - keys
            - maybe keys actually just exist in the top corner
        - pieces of a broken jewel
        - money?
        - food/enemy drops
    - main menu √
        - add buttons and text
    - pause menu √
        - add buttons and text
    - come up with a name
    - ...
    - .....
    - ???
    - profit
'''


pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
display = pygame.Surface((WIDTH, HEIGHT))

stateManager.push(PlayState())

running = True
while running:
    clock.tick()
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