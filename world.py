from utils import *
import json

camera = Camera()

class World:
    def __init__(self) -> None:
        with open("map.json") as f:
            content = json.load(f)
            self.backgroundMap = content["backgroundMap"]
            self.foregroundMap = content["foregroundBarriers"]
        self.tileSize = 60
        # bg_colors = [(0,0,50), (10,10,60)]
        # fg_colors = [(60,60,120)]
        # self.tile_colors = [bg_colors, fg_colors]
        for i in range(len(self.backgroundMap)):
            for j in range(len(self.backgroundMap[i])):
                self.backgroundMap[i][j] = BackgroundTile(j, i, self.backgroundMap[i][j])
        for i in range(len(self.foregroundMap)):
            for j in range(len(self.foregroundMap[i])):
                if self.foregroundMap[i][j] != 0:
                    self.foregroundMap[i][j] = ForegroundTile(j, i, self.foregroundMap[i][j])

    def render(self, screen):
        for i in range(len(self.backgroundMap)):
            for j in range(len(self.backgroundMap[i])):
                self.backgroundMap[i][j].drawTile(screen)
                if self.foregroundMap[i][j] != 0:
                    self.foregroundMap[i][j].drawTile(screen)




                # r = pygame.Rect(j * self.tileSize, i * self.tileSize, self.tileSize, self.tileSize)
                # bg_tile = self.backgroundMap[i][j]
                # fg_tile = self.foregroundMap[i][j]
                # # draw_tile(j, i, bg_tile, )
                # # draw_tile(j, i, fg_tile)
                # if self.backgroundMap[i][j] == 0:
                #     r = pygame.Rect(j * self.tileSize, i * self.tileSize, self.tileSize, self.tileSize)
                #     pygame.draw.rect(screen, (0,0,50), camera.project(r))
                    
                # elif self.backgroundMap[i][j] == 1:
                #     r = pygame.Rect(j * self.tileSize, i * self.tileSize, self.tileSize, self.tileSize)
                #     pygame.draw.rect(screen, (10,10,60), camera.project(r))
                    
                # if self.foregroundMap[i][j] == 1:
                #     r = pygame.Rect(j * self.tileSize, i * self.tileSize, self.tileSize, self.tileSize)
                #     pygame.draw.rect(screen, (60,60,120), camera.project(r))


# TODO: Make tile class
# Tile: x, y, type, rect, 


class Tile:
    tileSize = 60
    def __init__(self, x, y, type) -> None:
        self.rect: pygame.Rect = pygame.Rect(x*Tile.tileSize, y*Tile.tileSize, Tile.tileSize, Tile.tileSize)
        self.surf: pygame.Surface = pygame.Surface(self.rect.size)
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


