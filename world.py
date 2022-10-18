from utils import *
import json

camera = Camera()

class Chunk:
    def __init__(self) -> None:
        with open("map.json") as f:
            content = json.load(f)
            self.backgroundMap = content["chunk1"]["backgroundMap"]
            self.foregroundMap = content["chunk1"]["foregroundBarriers"]
        self.tileSize = 60
        for i in range(len(self.backgroundMap)):
            for j in range(len(self.backgroundMap[i])):
                self.backgroundMap[i][j] = BackgroundTile(j, i, self.backgroundMap[i][j])
                if self.foregroundMap[i][j] != 0:
                    self.foregroundMap[i][j] = ForegroundTile(j, i, self.foregroundMap[i][j])


    def render(self, screen):
        for i in range(len(self.backgroundMap)):
            for j in range(len(self.backgroundMap[i])):
                self.backgroundMap[i][j].drawTile(screen)
                if self.foregroundMap[i][j] != 0:
                    self.foregroundMap[i][j].drawTile(screen)


class Tile:
    tileSize = 70
    def __init__(self, x, y, type) -> None:
        self.rect: pygame.Rect = pygame.Rect(x*Tile.tileSize, y*Tile.tileSize, Tile.tileSize, Tile.tileSize)
        self.surf: pygame.Surface = pygame.Surface(self.rect.size)
        self.type = type
        self.color = (255,255,255)
    
    def drawTile(self, surface):
        surface.blit(self.surf, camera.project(self.rect).topleft)


class BackgroundTile(Tile):
    colors = [(0,0,50), (10,10,60)]
    def __init__(self, x, y, type) -> None:
        super().__init__(x, y, type)
        self.color = BackgroundTile.colors[type]
        self.surf.fill(self.color)

class ForegroundTile(Tile):
    colors = [(60,60,120)]
    def __init__(self, x, y, type) -> None:
        super().__init__(x, y, type)
        self.color = ForegroundTile.colors[type-1]
        self.surf.fill(self.color)


