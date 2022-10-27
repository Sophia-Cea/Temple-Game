import pygame
import sys
from utils import *
import json
# import tkinter as tk
# from tkinter import filedialog

# tk.Tk().withdraw()
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
file = "map.json"

class LevelEditor:
    def __init__(self) -> None:
        with open(file) as f:
            self.world = json.load(f)
        self.chunks = []
        for key in self.world:
            self.chunks.append(Chunk(self.world[key]))
        self.currentChunk = 0
        self.texts = [Text("Level Editor", "subtitle", (255,255,255), (50,1), True), Text("Chunk: " + str(self.currentChunk+1), "paragraph", (255,255,255), (50, 8), True), Text("Foreground", "paragraph", (255,255,255), (50, 87), True)]
        self.selectedColor = 1


    def render(self, screen):
        screen.fill((0,0,0))
        for text in self.texts:
            text.draw(screen)
        self.chunks[self.currentChunk].render(screen)

        for key in Chunk.tiles:
            screen.blit(pygame.transform.scale(Chunk.tiles[key], (50, 50)), (10, (HEIGHT - len(Chunk.tiles)*56)/2 + (key-1)*56))
            if key == self.selectedColor:
                pygame.draw.rect(screen, (255,0,0), pygame.Rect(10, (HEIGHT - len(Chunk.tiles)*56)/2 + (key-1)*56, 50,50), 3)

    def update(self):
        self.chunks[self.currentChunk].update()

    def handleInput(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.selectedColor = 1
                elif event.key == pygame.K_2:
                    self.selectedColor = 2
                elif event.key == pygame.K_3:
                    self.selectedColor = 3

                elif event.key == pygame.K_LEFT:
                    if self.currentChunk == 0:
                        self.currentChunk = len(self.chunks)-1
                    else:
                        self.currentChunk -= 1
                    self.texts[1].reset((255,255,255), "Chunk: " + str(1+self.currentChunk))
                elif event.key == pygame.K_RIGHT:
                    if self.currentChunk == len(self.chunks)-1:
                        self.currentChunk = 0
                    else:
                        self.currentChunk += 1
                    self.texts[1].reset((255,255,255), "Chunk: " + str(1+self.currentChunk))

                elif event.key == pygame.K_UP:
                    if self.chunks[self.currentChunk].currentMap == len(self.chunks[self.currentChunk].maps) - 1:
                        self.chunks[self.currentChunk].currentMap = 0
                    else:
                        self.chunks[self.currentChunk].currentMap += 1
                    self.texts[2].reset((255,255,255), ["foreground", "background", "enemies"][self.chunks[self.currentChunk].currentMap])
                elif event.key == pygame.K_DOWN:
                    if self.chunks[self.currentChunk].currentMap == 0:
                        self.chunks[self.currentChunk].currentMap = len(self.chunks[self.currentChunk].maps) - 1
                    else:
                        self.chunks[self.currentChunk].currentMap -= 1
                    self.texts[2].reset((255,255,255), ["foreground", "background", "enemies"][self.chunks[self.currentChunk].currentMap])
                
                elif event.key == pygame.K_RETURN:
                    saveFile()

                elif event.key == pygame.K_w:
                    newRow = []
                    for _ in range(len(self.chunks[self.currentChunk].maps[1][0])):
                        newRow.append(0)
                    self.chunks[self.currentChunk].maps[0].append(newRow)
                    self.chunks[self.currentChunk].maps[1].append(newRow)
                    self.chunks[self.currentChunk].gridSize[1] += 1
                    self.chunks[self.currentChunk].initializeGrid()
                elif event.key == pygame.K_s: # this is all fucked up and i dont know why ;n;
                    self.chunks[self.currentChunk].maps[0].pop(-1) #= self.chunks[self.currentChunk].maps[0][:-1]
                    self.chunks[self.currentChunk].maps[1].pop(-1) #= self.chunks[self.currentChunk].maps[1][:-1]
                    self.chunks[self.currentChunk].gridSize[1] -= 1
                    self.chunks[self.currentChunk].initializeGrid()
                elif event.key == pygame.K_d:
                    for i in range(len(self.chunks[self.currentChunk].maps[1])):
                        self.chunks[self.currentChunk].maps[1][i].append(0)
                        self.chunks[self.currentChunk].maps[0][i].append(0)
                    self.chunks[self.currentChunk].gridSize[0] += 1
                    self.chunks[self.currentChunk].initializeGrid()
                elif event.key == pygame.K_a:
                    for i in range(len(self.chunks[self.currentChunk].maps[1])):
                        self.chunks[self.currentChunk].maps[1][i].pop(-1)
                        self.chunks[self.currentChunk].maps[0][i].pop(-1)
                    self.chunks[self.currentChunk].gridSize[0] -= 1
                    self.chunks[self.currentChunk].initializeGrid()
                    
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                if x in range(int(self.chunks[self.currentChunk].marginX), int(WIDTH-self.chunks[self.currentChunk].marginX)) and y in range(int(self.chunks[self.currentChunk].marginY), int(HEIGHT-self.chunks[self.currentChunk].marginY)):
                    self.chunks[self.currentChunk].handleInput(x,y, self.selectedColor)
                else: #means its outside the grid
                    for key in Chunk.tiles:
                        if pygame.Rect(10, (HEIGHT - len(Chunk.tiles)*56)/2 + (key-1)*56, 50,50).collidepoint((x,y)):
                            self.selectedColor = key
                    

class Chunk:
    maxGridWidth = 70   # percent of width
    maxGridHeight = 70
    tiles = {
        1: pygame.image.load("assets/tiles/tile_1.png"),
        2: pygame.image.load("assets/tiles/tile_2.png"),
        3: pygame.image.load("assets/tiles/tile_3.png"),
        4: pygame.image.load("assets/tiles/tile_4.png"),
        5: pygame.image.load("assets/tiles/tile_5.png"),
        6: pygame.image.load("assets/tiles/tile_6.png"),
        7: pygame.image.load("assets/tiles/tile_7.png"),
        8: pygame.image.load("assets/tiles/tile_8.png"),
        9: pygame.image.load("assets/tiles/tile_9.png"),
        10: pygame.image.load("assets/tiles/tile_10.png"),
        11: pygame.image.load("assets/tiles/tile_11.png")
    }
    def __init__(self, chunkDict) -> None:
        self.chunkDict = chunkDict
        self.foreground = chunkDict["foregroundBarriers"]
        self.background = chunkDict["backgroundMap"]
        self.enemies = chunkDict["enemies"]
        self.gridSize = [len(self.foreground[0]), len(self.foreground)]
        self.tileSize = None
        self.marginX = None
        self.marginY = None
        self.initializeGrid()
        self.maps = [self.foreground, self.background, self.enemies]
        self.currentMap = 0

    def render(self, screen):
        for i in range(self.gridSize[1]):
            for j in range(self.gridSize[0]):
                if self.maps[self.currentMap][i][j] != 0:
                    screen.blit(pygame.transform.scale(Chunk.tiles[self.maps[self.currentMap][i][j]], (self.tileSize, self.tileSize)), (self.marginX+j*self.tileSize, self.marginY+i*self.tileSize))
                    # pygame.draw.rect(screen, Chunk.tiles[self.maps[self.currentMap][i][j]], pygame.Rect(self.marginX+j*self.tileSize, self.marginY+i*self.tileSize, self.tileSize, self.tileSize))
        for i in range(self.gridSize[0]+1):
            pygame.draw.line(screen, (255,255,255), (self.marginX + i*self.tileSize, self.marginY), (self.marginX + i*self.tileSize, HEIGHT-self.marginY), 1)
        for j in range(self.gridSize[1]+1):
            pygame.draw.line(screen, (255,255,255), (self.marginX, self.marginY + j*self.tileSize), (WIDTH-self.marginX, self.marginY + j*self.tileSize), 1)

    def update(self):
        pass

    def handleInput(self, x,y, selectedColor):
        x = int((x- self.marginX)/self.tileSize)
        y = int((y - self.marginY)/self.tileSize)
        if self.maps[self.currentMap][y][x] != selectedColor:
            if x >= 0 and x < self.gridSize[0] and y >= 0 and y < self.gridSize[1]:
                self.maps[self.currentMap][y][x] = selectedColor
        else:
            self.maps[self.currentMap][y][x] = 0

    def findTileSize(self):
        maxWidth = WIDTH*Chunk.maxGridWidth/100
        maxHeight = HEIGHT*Chunk.maxGridHeight/100
        tileSizes = [maxWidth/len(self.foreground[0]), maxHeight/len(self.foreground)]
        print("finding tile size...")
        return min(tileSizes)

    def calculateMargin(self):
        self.marginX = (WIDTH - (self.tileSize*self.gridSize[0]))/2
        self.marginY = (HEIGHT - (self.tileSize*self.gridSize[1]))/2

    def initializeGrid(self):
        self.tileSize = self.findTileSize()
        self.calculateMargin()



def saveFile():
    for i in enumerate(levelEditor.world):
        levelEditor.world[i[1]]["backgroundMap"] = levelEditor.chunks[i[0]].background
        levelEditor.world[i[1]]["foregroundBarriers"] = levelEditor.chunks[i[0]].foreground
        levelEditor.world[i[1]]["enemies"] = levelEditor.chunks[i[0]].enemies
    with open(file, "w") as f:
        json.dump(levelEditor.world, f)

def render(screen):
    levelEditor.render(screen)

def update():
    global file_path
    levelEditor.update()

def handleInput(events):
    levelEditor.handleInput(events)

def run(screen, events):
    render(screen)
    update()
    handleInput(events)

running = True
# file_path = filedialog.askopenfilename(title="Select Level File",
#                             filetypes=[("JSON Files", "*.json")],
#                             defaultextension="json")
# if file_path is None:
#     pygame.quit()
#     sys.exit()
# past this point, the file definitely exists (program terminates otherwise) 
    
levelEditor = LevelEditor() 

while running:
    clock.tick()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            saveFile()
            pygame.quit()
            sys.exit()
        

    WIDTH, HEIGHT = screen.get_size()
    run(screen, events)
    pygame.display.flip()