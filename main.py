import pygame
import sys
from state import *

# TODO next:
# refactor the enemy handling system so that they are in the json map, 
# and they are generated in the world and handled in the world (render, update)

# TODO find where handleBarrierCollision is called and update parameters

# ask andrew:
# how should the player be able to control where they shoot?
# should the player be free to move all over the screen (including diagonals) or only up/down left/right?
# how should the camera move? just follow the player anywhere they go or be more 
# steady and stop at the edges and stuff? (ask sophia for detailed description of this)
# can i make Player, world, and camera static?

'''
    TODO
    - make player controller
        - How do you control what direction the bullet shoots?
    - make level editor √
    - rework camera
    - enemies
        - move enemies from playstate to being generated in the chunk
        - ***** refactor the playstate to have 4 chunks that are run based on which chunk ur in
    - attacks
    - weapon switching
    - player health and damage
    - enemy health and damage
    - inventory
        - keys
            - maybe keys actually just exist in the top corner
        - pieces of a broken jewel
    - main menu
    - pause menu
    - ...
    - .....
    - ???
    - profit
'''


pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
display = pygame.Surface((WIDTH, HEIGHT))
stateManager = StateManager()

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