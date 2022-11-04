from utils import *


class Tile:
    tileSize = 64
    tileList = []
    def __init__(self, x, y, type) -> None:
        self.rect: pygame.Rect = pygame.Rect(x*Tile.tileSize, y*Tile.tileSize, Tile.tileSize, Tile.tileSize)
        self.surf: pygame.Surface = pygame.Surface(self.rect.size)
        self.type = type
        Tile.tileList.append(self)
    
    def drawTile(self, surface):
        surface.blit(self.surf, camera.project(self.rect).topleft)

class BackgroundTile(Tile):
    tiles = {
        0: pygame.Surface((16,16)),
        1: pygame.image.load("assets/tiles/tile_2.png"),
        2: pygame.image.load("assets/tiles/tile_3.png"),
        3: pygame.image.load("assets/tiles/tile_4.png"),
        4: pygame.image.load("assets/tiles/tile_5.png"),
        5: pygame.image.load("assets/tiles/tile_6.png"),
        6: pygame.image.load("assets/tiles/tile_7.png"),
        7: pygame.image.load("assets/tiles/tile_8.png"),
        8: pygame.image.load("assets/tiles/tile_9.png"),
        9: pygame.image.load("assets/tiles/tile_10.png"),
        10: pygame.image.load("assets/tiles/tile_11.png"),
        11: pygame.image.load("assets/tiles/tile_15.png"),
        12: pygame.image.load("assets/tiles/tile_16.png"),
        13: pygame.image.load("assets/tiles/tile_17.png"),
        14: pygame.image.load("assets/tiles/tile_18.png")
    }
    def __init__(self, x, y, type) -> None:
        super().__init__(x, y, type)
        self.surf = pygame.transform.scale(BackgroundTile.tiles[type], (Tile.tileSize, Tile.tileSize))

class ForegroundTile(Tile):
    tiles = {
        1: pygame.image.load("assets/tiles/brick.png"),
        2: pygame.image.load("assets/tiles/brick_top.png"),
        3: pygame.image.load("assets/tiles/brick_left.png"),
        4: pygame.image.load("assets/tiles/brick_right.png"),
        5: pygame.image.load("assets/tiles/brick_u.png"),
        6: pygame.image.load("assets/tiles/tile_12.png"),
        7: pygame.image.load("assets/tiles/tile_13.png")

    }
    def __init__(self, x, y, type) -> None:
        super().__init__(x, y, type)
        self.surf = pygame.transform.scale(ForegroundTile.tiles[type], (Tile.tileSize, Tile.tileSize))

class AnimatedTile(Tile):
    tiles = {
        1: [
            pygame.transform.scale(pygame.image.load("assets/decorativeItems/torch_1.png"), (Tile.tileSize, Tile.tileSize)),
            pygame.transform.scale(pygame.image.load("assets/decorativeItems/torch_2.png"), (Tile.tileSize, Tile.tileSize)),
            pygame.transform.scale(pygame.image.load("assets/decorativeItems/torch_3.png"), (Tile.tileSize, Tile.tileSize)),
            pygame.transform.scale(pygame.image.load("assets/decorativeItems/torch_4.png"), (Tile.tileSize, Tile.tileSize))

        ]
    }
    def __init__(self, x, y, type) -> None:
        super().__init__(x, y, type)
        print(type)
        try:
            self.animation = AnimatedTile.tiles[type] #TODO update this
        except:
            self.animation = AnimatedTile.tiles[1]
        self.currentFrame = 0
        self.frameFrq = 10
        self.counter = 0

    def drawTile(self, surface):
        surface.blit(self.animation[self.currentFrame], camera.projectPoint(self.rect.topleft))
    
    def update(self):
        if self.counter < self.frameFrq:
            self.counter += 1
        else:
            self.counter = 0
            if self.currentFrame < len(self.animation)-1:
                self.currentFrame += 1
            else:
                self.currentFrame = 0

class DecorativeTile(Tile):
    tiles = {
        1: pygame.transform.scale(pygame.image.load("assets/decorativeItems/colum_1.png"), (Tile.tileSize, Tile.tileSize*3))
    }
    def __init__(self, x, y, type) -> None:
        super().__init__(x, y, type)

