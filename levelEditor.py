import pygame
import sys
from utils import *
import json

colorGrid = {
    1: (150,150,200),
    2: (200,150,150),
    3: (150,200,150)
}

activeColor = 1

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)

with open("testMap.json") as f:
    world = json.load(f)

gridDimensions = [len(world["chunk1"]["backgroundMap"][0]),len(world["chunk1"]["backgroundMap"])]
# grid = []

# for i in range(gridDimensions[1]):
#     temp = []
#     for j in range(gridDimensions[0]):
#         temp.append(0)
#     grid.append(temp)

# print(len(grid))
# print(len(grid[0]))

grid = world["chunk1"]["foregroundBarriers"]

squareSize = HEIGHT/gridDimensions[1]
margin = (WIDTH - squareSize*gridDimensions[0])/2

def render(screen):
    screen.fill((0,0,0))
    for key in colorGrid:
        pygame.draw.rect(screen, colorGrid[key], pygame.Rect(2, (HEIGHT-(34*len(colorGrid)))/2 + 34 * (key-1), 30, 30))
        if key == activeColor:
            pygame.draw.rect(screen, (255,0,0), pygame.Rect(2, (HEIGHT-(34*len(colorGrid)))/2 + 34 * (key-1), 30, 30), 3)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != 0:
                pygame.draw.rect(screen, colorGrid[grid[i][j]], pygame.Rect(margin+j*squareSize, i*squareSize, squareSize, squareSize))

    for i in range(gridDimensions[0]+1):
        pygame.draw.line(screen, (255,255,255), (margin + squareSize*i, 0), (margin + squareSize*i, HEIGHT), 1)
    for i in range(gridDimensions[1]+1):
        pygame.draw.line(screen, (255,255,255), (margin, squareSize*i), (WIDTH-margin, squareSize*i), 1)


def update():
    pass


def handleInput(events):
    global activeColor
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            for key in colorGrid:
                if pygame.Rect(2, (HEIGHT-(34*len(colorGrid)))/2 + 34 * (key-1), 30, 30).collidepoint((x,y)):
                    activeColor = key
            if x >= margin:
                x = int((x-margin)/squareSize)
                y = int(y/squareSize)
                print(x,y)
                if x<len(grid[0]) and y < len(grid):
                    if grid[y][x] != activeColor:
                        grid[y][x] = activeColor
                    else: 
                        grid[y][x] = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                activeColor = 1
            elif event.key == pygame.K_2:
                activeColor = 2
            elif event.key == pygame.K_3:
                activeColor = 3


def run(screen, events):
    render(screen)
    update()
    handleInput(events)



running = True
while running:
    clock.tick()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                world["chunk1"]["foregroundBarriers"] = grid
                world["chunk1"]["backgroundMap"] = grid
                with open("testMap.json", "w") as f:
                    json.dump(world, f)

    WIDTH, HEIGHT = screen.get_size()
    run(screen, events)
    pygame.display.flip()