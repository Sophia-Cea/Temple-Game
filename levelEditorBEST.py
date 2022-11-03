from entity import FixedEnemy
from tile import *
import json

foregroundList: list = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
    [1,1,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1]
]

backgroundList: list = []

for i in range(len(foregroundList)):
    ye = []
    for j in range(len(foregroundList[0])):
        ye.append(foregroundList[i][j])
    backgroundList.append(ye)

file = "levelEditorFile.json"
screen = pygame.display.set_mode([1000, 700], pygame.RESIZABLE)
animatedTiles = {}
for key in AnimatedTile.tiles:
    animatedTiles[int(key)] = AnimatedTile.tiles[key][0]


class LevelEditor:
    def __init__(self) -> None:
        self.room = Room()
        self.texts = [Text("Level Editor", "subtitle", (255,255,255), (50,1), True), Text("Foreground", "paragraph", (255,255,255), (50, 87), True)]
        self.selectedTile = 1
        self.mapNames = ["foreground", "background", "enemies", "decorations"]
        self.isDrawing = False
        self.erasing = False
        self.spacing = 10
        self.marginX = 10
        self.marginY = 10
        self.calculateMenuTileSize()

    def calculateMenuTileSize(self):
        # self.menuTileSize = ((HEIGHT - 2*self.marginY)/(len(self.room.getCurrentTileList()))) - self.spacing
        self.menuTileSize = 25

    def render(self, screen):
        screen.fill((0,0,0))
        for text in self.texts:
            text.draw(screen)
        self.room.render(screen)

        for key in self.room.getCurrentTileList():
            screen.blit(pygame.transform.scale(self.room.getCurrentTileList()[key], (self.menuTileSize, self.menuTileSize)), (self.marginX, (self.marginY + (int(key)-1)*(self.menuTileSize+self.spacing))))
            if key == self.selectedTile:
                pygame.draw.rect(screen, (255,0,0), pygame.Rect(self.marginX, (self.marginY + (key-1)*(self.menuTileSize+self.spacing)), self.menuTileSize, self.menuTileSize), 3)

    def update(self):
        if self.isDrawing:
            self.room.update(self.selectedTile)

    def handleInput(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.calculateMenuTileSize()
                    if self.room.currentMap == len(self.room.maps) - 1:
                        self.room.currentMap = 0
                    else:
                        self.room.currentMap += 1
                    self.texts[1].reset((255,255,255), self.mapNames[self.room.currentMap])
                elif event.key == pygame.K_DOWN:
                    self.calculateMenuTileSize()
                    if self.room.currentMap == 0:
                        self.room.currentMap = len(self.room.maps) - 1
                    else:
                        self.room.currentMap -= 1
                    self.texts[1].reset((255,255,255), self.mapNames[self.room.currentMap])
                
                elif event.key == pygame.K_RETURN:
                    saveFile()

                elif event.key == pygame.K_1:
                    self.erasing = False
                
                elif event.key == pygame.K_2:
                    self.erasing = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if x in range(int(self.room.marginX), int(WIDTH-self.room.marginX)) and y in range(int(self.room.marginY), int(HEIGHT-self.room.marginY)):
                    self.isDrawing = True
                else: #means its outside the grid
                    for key in self.room.getCurrentTileList():
                        if pygame.Rect(self.marginX, self.marginY + (key-1)*(self.menuTileSize+self.spacing), self.menuTileSize,self.menuTileSize).collidepoint((x,y)):
                            self.selectedTile = key 
            if event.type == pygame.MOUSEBUTTONUP:   
                self.isDrawing = False



class Room:
    maxGridWidth = 70   # percent of width
    maxGridHeight = 70
    def __init__(self) -> None:
        self.foreground = foregroundList.copy()
        self.background = backgroundList.copy()
        self.enemies = self.convertMapToZeroes()
        self.decorations = self.convertMapToZeroes()
        self.gridSize = [len(self.foreground[0]), len(self.foreground)]
        self.tileSize = None
        self.marginX = None
        self.marginY = None
        self.initializeGrid()
        self.maps = [self.foreground, self.background, self.enemies, self.decorations]
        self.currentMap = 0
        self.tileLists = [ForegroundTile.tiles, BackgroundTile.tiles, {"1":pygame.image.load("assets/enemies/nut_devil_1.png")}, animatedTiles]

    def getCurrentTileList(self):
        return self.tileLists[self.currentMap]
    
    def getCurrentMap(self):
        return self.maps[self.currentMap]

    def convertMapToZeroes(self):
        yee = []
        for i in range(len(foregroundList)):
            ye = []
            for j in range(len(foregroundList[0])):
                ye.append(0)
            yee.append(ye)
        return yee

    def render(self, screen):
        for i in range(self.gridSize[1]):
            for j in range(self.gridSize[0]):
                if self.maps[self.currentMap][i][j] != 0:
                    screen.blit(pygame.transform.scale(self.getCurrentTileList()[self.maps[self.currentMap][i][j]], (self.tileSize, self.tileSize)), (self.marginX+j*self.tileSize, self.marginY+i*self.tileSize))
        for i in range(self.gridSize[0]+1):
            pygame.draw.line(screen, (255,255,255), (self.marginX + i*self.tileSize, self.marginY), (self.marginX + i*self.tileSize, HEIGHT-self.marginY), 1)
        for j in range(self.gridSize[1]+1):
            pygame.draw.line(screen, (255,255,255), (self.marginX, self.marginY + j*self.tileSize), (WIDTH-self.marginX, self.marginY + j*self.tileSize), 1)

    def update(self, selectedTile):
        x, y = pygame.mouse.get_pos()
        x = int((x- self.marginX)/self.tileSize)
        y = int((y - self.marginY)/self.tileSize)
        if levelEditor.erasing:
            if x >= 0 and x < self.gridSize[0] and y >= 0 and y < self.gridSize[1]:
                self.getCurrentMap()[y][x] = 0
        else:
            if x >= 0 and x < self.gridSize[0] and y >= 0 and y < self.gridSize[1]:
                self.getCurrentMap()[y][x] = selectedTile

    def handleInput(self):
        pass

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


roomDict = {}
def saveFile():
    roomDict["backgroundMap"] = levelEditor.room.background
    roomDict["foregroundBarriers"] = levelEditor.room.foreground
    roomDict["enemies"] = levelEditor.room.enemies
    roomDict["decoration"] = levelEditor.room.decorations
    with open(file, "w") as f:
        json.dump(roomDict, f)

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
            pygame.quit()
            sys.exit()
        

    WIDTH, HEIGHT = screen.get_size()
    run(screen, events)
    pygame.display.flip()


