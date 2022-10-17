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
        bg_colors = [(0,0,50), (10,10,60)]
        fg_colors = [(60,60,120)]
        self.tile_colors = [bg_colors, fg_colors]

    def render(self, screen):
        for i in range(len(self.backgroundMap)):
            for j in range(len(self.backgroundMap[i])):
                r = pygame.Rect(j * self.tileSize, i * self.tileSize, self.tileSize, self.tileSize)
                bg_tile = self.backgroundMap[i][j]
                fg_tile = self.foregroundMap[i][j]
                # draw_tile(j, i, bg_tile, )
                # draw_tile(j, i, fg_tile)
                if self.backgroundMap[i][j] == 0:
                    r = pygame.Rect(j * self.tileSize, i * self.tileSize, self.tileSize, self.tileSize)
                    pygame.draw.rect(screen, (0,0,50), camera.project(r))
                    
                elif self.backgroundMap[i][j] == 1:
                    r = pygame.Rect(j * self.tileSize, i * self.tileSize, self.tileSize, self.tileSize)
                    pygame.draw.rect(screen, (10,10,60), camera.project(r))
                    
                if self.foregroundMap[i][j] == 1:
                    r = pygame.Rect(j * self.tileSize, i * self.tileSize, self.tileSize, self.tileSize)
                    pygame.draw.rect(screen, (60,60,120), camera.project(r))

    def draw_tile(x, y, type):
        pass



# TODO: Make tile class
# Tile: x, y, type, rect, 