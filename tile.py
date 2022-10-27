from utils import *


class Tile:
    tileSize = 70
    def __init__(self, x, y, type) -> None:
        self.rect: pygame.Rect = pygame.Rect(x*Tile.tileSize, y*Tile.tileSize, Tile.tileSize, Tile.tileSize)
        self.surf: pygame.Surface = pygame.Surface(self.rect.size)
        self.type = type
    
    def drawTile(self, surface):
        surface.blit(self.surf, camera.project(self.rect).topleft)


class BackgroundTile(Tile):
    tiles = {
        0: pygame.Surface((16,16)),
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
        11: pygame.image.load("assets/tiles/tile_11.png"),
        12: pygame.image.load("assets/tiles/tile_12.png"),
        13: pygame.image.load("assets/tiles/tile_13.png"),
        14: pygame.image.load("assets/tiles/tile_14.png"),
        15: pygame.image.load("assets/tiles/tile_15.png")
    }
    def __init__(self, x, y, type) -> None:
        super().__init__(x, y, type)
        print(type)
        self.surf = pygame.transform.scale(BackgroundTile.tiles[type], (Tile.tileSize, Tile.tileSize))

class ForegroundTile(Tile):
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
        11: pygame.image.load("assets/tiles/tile_11.png"),
        12: pygame.image.load("assets/tiles/tile_12.png"),
        13: pygame.image.load("assets/tiles/tile_13.png"),
        14: pygame.image.load("assets/tiles/tile_14.png"),
        15: pygame.image.load("assets/tiles/tile_15.png")
    }
    def __init__(self, x, y, type) -> None:
        super().__init__(x, y, type)
        self.surf = pygame.transform.scale(ForegroundTile.tiles[type], (Tile.tileSize, Tile.tileSize))


