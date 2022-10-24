from utils import *


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


