import pygame
import sys
from utils import *
import json


pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)

class LevelEditor:
    def __init__(self) -> None:
        with open("testMap.json") as f:
            self.world = json.load(f)
        self.chunks = [Chunk(self.world["chunk1"]), Chunk(self.world["chunk2"]), Chunk(self.world["chunk3"]), Chunk(self.world["chunk4"])]
        self.currentChunk = 0
        self.texts = [Text("Level Editor", "subtitle", (255,255,255), (50,1), True), Text("Chunk: " + str(self.currentChunk+1), "paragraph", (255,255,255), (50, 8), True), Text("Foreground", "paragraph", (255,255,255), (50, 87), True)]
        self.selectedColor = 1

    def render(self, screen):
        screen.fill((0,0,0))
        for text in self.texts:
            text.draw(screen)
        self.chunks[self.currentChunk].render(screen)

        for key in Chunk.colors:
            pygame.draw.rect(screen, Chunk.colors[key], pygame.Rect(10, (HEIGHT - len(Chunk.colors)*56)/2 + (key-1)*56, 50,50))
            if key == self.selectedColor:
                pygame.draw.rect(screen, (255,0,0), pygame.Rect(10, (HEIGHT - len(Chunk.colors)*56)/2 + (key-1)*56, 50,50), 3)

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
                    self.texts[2].reset((255,255,255), ["foreground", "background"][self.chunks[self.currentChunk].currentMap])

                elif event.key == pygame.K_DOWN:
                    if self.chunks[self.currentChunk].currentMap == 0:
                        self.chunks[self.currentChunk].currentMap = len(self.chunks[self.currentChunk].maps) - 1
                    else:
                        self.chunks[self.currentChunk].currentMap -= 1
                    self.texts[2].reset((255,255,255), ["foreground", "background"][self.chunks[self.currentChunk].currentMap])
                    
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                if x in range(int(self.chunks[self.currentChunk].marginX), int(WIDTH-self.chunks[self.currentChunk].marginX)) and y in range(int(self.chunks[self.currentChunk].marginY), int(HEIGHT-self.chunks[self.currentChunk].marginY)):
                    self.chunks[self.currentChunk].handleInput(x,y, self.selectedColor)
                else: #means its outside the grid
                    for key in Chunk.colors:
                        if pygame.Rect(10, (HEIGHT - len(Chunk.colors)*56)/2 + (key-1)*56, 50,50).collidepoint((x,y)):
                            self.selectedColor = key
                    

class Chunk:
    maxGridWidth = 70   # percent of width
    maxGridHeight = 70
    colors = {
        1: (150,150,200),
        2: (200,150,150),
        3: (150,200,150)
    }
    def __init__(self, chunkDict) -> None:
        self.chunkDict = chunkDict
        self.foreground = chunkDict["foregroundBarriers"]
        self.background = chunkDict["backgroundMap"]
        self.gridSize = [len(self.foreground[0]), len(self.foreground)]
        self.tileSize = self.findTileSize()
        self.marginX = (WIDTH - (self.tileSize*self.gridSize[0]))/2
        self.marginY = (HEIGHT - (self.tileSize*self.gridSize[1]))/2
        self.maps = [self.foreground, self.background]
        self.currentMap = 0

    def render(self, screen):
        for i in range(self.gridSize[1]):
            for j in range(self.gridSize[0]):
                if self.maps[self.currentMap][i][j] != 0:
                    pygame.draw.rect(screen, Chunk.colors[self.maps[self.currentMap][i][j]], pygame.Rect(self.marginX+j*self.tileSize, self.marginY+i*self.tileSize, self.tileSize, self.tileSize))
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
        return min(tileSizes)



levelEditor = LevelEditor()


def render(screen):
    levelEditor.render(screen)

def update():
    levelEditor.update()

def handleInput(events):
    levelEditor.handleInput(events)

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

    WIDTH, HEIGHT = screen.get_size()
    run(screen, events)
    pygame.display.flip()