# from utils import *
import json
from entity import *

# camera = Camera()
file = "map.json"
player = Player()

class World:
    def __init__(self) -> None:
        with open(file) as f:
            self.world = json.load(f)
        self.chunks = []
        for key in self.world:
            self.chunks.append(Chunk(self.world[key]))
        self.currentChunk = 0
    
    def getCurrentChunk(self):
        return self.chunks[self.currentChunk]
    
    def render(self, screen):
        self.getCurrentChunk().render(screen)
        for i in range(player.health):
            pygame.draw.circle(screen, (255,0,0), (35+i*30, 30), 10)

    def update(self):
        self.getCurrentChunk().update()
        Bullet.checkAllBulletsCollision(self.getCurrentChunk().foregroundMap, player)

    def handleInput(self, events):
        self.getCurrentChunk().handleInput(events)

class Chunk:
    def __init__(self, chunkDict) -> None:
        self.chunkDict = chunkDict
        self.backgroundMap = chunkDict["backgroundMap"]
        self.foregroundMap = chunkDict["foregroundBarriers"]
        self.enemyMap = chunkDict["enemies"]
        self.enemies = []
        for i in range(len(self.backgroundMap)):
            for j in range(len(self.backgroundMap[i])):
                self.backgroundMap[i][j] = BackgroundTile(j, i, self.backgroundMap[i][j])
                if self.foregroundMap[i][j] != 0:
                    self.foregroundMap[i][j] = ForegroundTile(j, i, self.foregroundMap[i][j])
                if self.enemyMap[i][j] != 0:
                    if self.enemyMap[i][j] == 1:
                        self.enemies.append(FixedEnemy((i,j), randint(500,5000)))


    def render(self, screen):
        for i in range(len(self.backgroundMap)):
            for j in range(len(self.backgroundMap[i])):
                self.backgroundMap[i][j].drawTile(screen)
                if self.foregroundMap[i][j] != 0:
                    self.foregroundMap[i][j].drawTile(screen)
        for enemy in self.enemies:
            enemy.render(screen)
        
    def update(self):
        for enemy in self.enemies:
            enemy.update()
            if enemy.readyToLaunch:
                if measureDistance(enemy.pos, player.pos) <= 200:
                    enemy.launchBullet(player.rect.center)

    def handleInput(self, events):
        for enemy in self.enemies:
            enemy.handleInput(events)
    

