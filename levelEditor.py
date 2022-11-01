import pygame
import sys
from tile import AnimatedTile, BackgroundTile, ForegroundTile
from utils import *
import json

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE)
file = "newMap.json"

enemyTiles = {
    1 : pygame.image.load("assets/enemies/nut_devil_1.png")
}

maps = ["foreground", "background", "enemies", "animated tiles"]

animatedTiles = {}
for i in enumerate(AnimatedTile.tiles):
    animatedTiles[i[0]+1] = AnimatedTile.tiles[i[1]][0]

class LevelEditor:
    def __init__(self) -> None:
        with open(file) as f:
            self.world = json.load(f)
        self.chunks = []
        for key in self.world:
            self.chunks.append(Chunk(self.world[key]))
        self.currentChunk = 0
        self.texts = [Text("Level Editor", "subtitle", (255,255,255), (50,1), True), Text("Chunk: " + str(self.currentChunk+1), "paragraph", (255,255,255), (50, 8), True), Text("Foreground", "paragraph", (255,255,255), (50, 87), True)]
        self.tileLists = [ForegroundTile.tiles, BackgroundTile.tiles, enemyTiles, animatedTiles]
        self.marginX = 10
        self.marginY = 10
        self.spacing = 10
        self.selectedTile = 1

    def calculateTilesize(self):
        self.tileSize = ((HEIGHT - 2*self.marginY)/(len(self.getCurrentTileList))) - self.spacing
    
    def getCurrentTileList(self):
        return self.tileLists[self.currentChunk]

    def getCurrentChunk(self):
        return self.chunks[self.currentChunk]

    def render(self, screen):
        screen.fill((0,0,0))
        for text in self.texts:
            text.draw(screen)
        self.getCurrentChunk().render(screen)

        for key in self.getCurrentTileList():
            screen.blit(pygame.transform.scale(self.getCurrentTileList()[key], (self.tileSize, self.tileSize)), (self.marginX, (self.marginY + (key-1)*(self.tileSize+self.spacing))))
            if key == self.selectedTile:
                pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.marginX, (self.marginY + (key-1)*(self.tileSize+self.spacing)), self.tileSize, self.tileSize), 3)

    def update(self):
        self.chunks[self.currentChunk].update()

    def handleInput(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.getCurrentChunk().currentRoom == 0:
                        self.getCurrentChunk().currentRoom = len(self.getCurrentChunk().rooms)-1
                    else:
                        self.getCurrentChunk().currentRoom -= 1
                    self.texts[1].reset((255,255,255), "Chunk: " + str(1+self.getCurrentChunk().currentRoom))
                elif event.key == pygame.K_RIGHT:
                    if self.getCurrentChunk().currentRoom == len(self.chunks)-1:
                        self.getCurrentChunk().currentRoom = 0
                    else:
                        self.getCurrentChunk().currentRoom += 1
                    self.texts[1].reset((255,255,255), "Chunk: " + str(1+self.getCurrentChunk().currentRoom))

                elif event.key == pygame.K_UP:
                    if self.getCurrentChunk().getCurrentRoom().currentMap == len(self.chunks[self.currentChunk].maps) - 1:
                        self.getCurrentChunk().getCurrentRoom().currentMap = 0
                    else:
                        self.getCurrentChunk().getCurrentRoom().currentMap += 1
                    self.texts[2].reset((255,255,255), maps[self.getCurrentChunk().getCurrentRoom().currentMap])
                elif event.key == pygame.K_DOWN:
                    if self.getCurrentChunk().getCurrentRoom().currentMap == 0:
                        self.getCurrentChunk().getCurrentRoom().currentMap = len(self.chunks[self.currentChunk].maps) - 1
                    else:
                        self.getCurrentChunk().getCurrentRoom().currentMap -= 1
                    self.texts[2].reset((255,255,255), maps[self.getCurrentChunk().getCurrentRoom().currentMap])
                
                elif event.key == pygame.K_RETURN:
                    saveFile()

                # BUG fix all of this broken stuff
                elif event.key == pygame.K_w:
                    newRow = []
                    for _ in range(len(self.chunks[self.currentChunk].maps[1][0])):
                        newRow.append(0)
                    self.chunks[self.currentChunk].maps[0].append(newRow)
                    self.chunks[self.currentChunk].maps[1].append(newRow)
                    self.chunks[self.currentChunk].gridSize[1] += 1
                    self.chunks[self.currentChunk].initializeGrid()
                elif event.key == pygame.K_s:
                    self.chunks[self.currentChunk].maps[0].pop(-1)
                    self.chunks[self.currentChunk].maps[1].pop(-1)
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

            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if x in range(int(self.getCurrentChunk().marginX), int(WIDTH-self.getCurrentChunk().marginX)) and y in range(int(self.getCurrentChunk().marginY), int(HEIGHT-self.getCurrentChunk().marginY)):
                    self.getCurrentChunk().handleInput(x,y, self.selectedTile)
                else: #means its outside the grid
                    for key in self.getCurrentTileList():
                        if pygame.Rect(self.marginX, self.marginY+(self.tileSize+self.spacing)*(key-1), self.tileSize, self.tileSize).collidepoint((x,y)):
                            self.selectedTile = key


class Chunk:
    def __init__(self, chunkDict) -> None:
        self.rooms = []
        self.chunkDict = chunkDict
        for room in self.chunkDict["rooms"]:
            self.rooms.append(Room(room))
        self.currentRoom = 0

    def getCurrentRoom(self):
        return self.rooms[self.currentRoom]
        
    def render(self, screen):
        return self.getCurrentRoom().render(screen)

    def update(self):
        return self.getCurrentRoom().update()

    def handleInput(self, x, y, selectedTile):
        return self.getCurrentRoom.handleInput(events)


class Room:
    maxGridWidth = 70   # percent of width
    maxGridHeight = 70
    def __init__(self, roomDict) -> None:
        self.roomDict = roomDict
        self.foreground = roomDict["foreground"]
        self.background = roomDict["background"]
        self.enemies = roomDict["enemies"]
        self.decorations = roomDict["decor"]
        self.maps = [self.foreground, self.background, self.enemies, self.decorations]
        self.currentMap = 0
        self.maps = []

        self.tileSize = None
        self.marginX = None
        self.marginY = None
        self.gridSize = [len(self.foreground[0]), len(self.foreground)]
        self.initializeGrid()
    
    def findTileSize(self):
        maxWidth = WIDTH*Room.maxGridWidth/100
        maxHeight = HEIGHT*Room.maxGridHeight/100
        tileSizes = [maxWidth/len(self.foreground[0]), maxHeight/len(self.foreground)]
        return min(tileSizes)

    def calculateMargin(self):
        self.marginX = (WIDTH - (self.tileSize*self.gridSize[0]))/2
        self.marginY = (HEIGHT - (self.tileSize*self.gridSize[1]))/2

    def initializeGrid(self):
        self.tileSize = self.findTileSize()
        self.calculateMargin()

    def render(self, screen):
        for i in range(self.gridSize[1]):
            for j in range(self.gridSize[0]):
                if self.maps[self.currentMap][i][j] != 0:
                    screen.blit(pygame.transform.scale(levelEditor.getCurrentTileList().tiles[self.maps[self.currentMap][i][j]], (self.tileSize, self.tileSize)), (self.marginX+j*self.tileSize, self.marginY+i*self.tileSize))
        for i in range(self.gridSize[0]+1):
            pygame.draw.line(screen, (255,255,255), (self.marginX + i*self.tileSize, self.marginY), (self.marginX + i*self.tileSize, HEIGHT-self.marginY), 1)
        for j in range(self.gridSize[1]+1):
            pygame.draw.line(screen, (255,255,255), (self.marginX, self.marginY + j*self.tileSize), (WIDTH-self.marginX, self.marginY + j*self.tileSize), 1)

    def update(self):
        pass

    def handleInput(self, events):
        pass



def saveFile(): #BUG refactor this to incorporate rooms
    for i in enumerate(levelEditor.world):
        levelEditor.world[i[1]]["backgroundMap"] = levelEditor.chunks[i[0]].background
        levelEditor.world[i[1]]["foregroundBarriers"] = levelEditor.chunks[i[0]].foreground
        levelEditor.world[i[1]]["enemies"] = levelEditor.chunks[i[0]].enemies
        levelEditor.world[i[1]]["decoration"] = levelEditor.chunks[i[0]].decorations
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
    
levelEditor = LevelEditor() 

while running:
    clock.tick()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            # saveFile()
            pygame.quit()
            sys.exit()
        

    WIDTH, HEIGHT = screen.get_size()
    run(screen, events)
    pygame.display.flip()