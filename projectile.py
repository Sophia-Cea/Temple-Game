# from playerStates import *
from tile import *

# world = Chunk()


class Projectile:
    def __init__(self) -> None:
        self.angle = None
        self.size = None
        self.speed = None
        self.color = None
        self.startPos = [0,0]
        self.pos = self.startPos

    def setVars(self, size, angle, speed, color, startPos):
        self.angle = angle
        self.size = size
        self.speed = speed
        self.color = color
        self.startPos = startPos
        self.pos = self.startPos

    def render(self, screen):
        pygame.draw.circle(screen, self.color, camera.projectPoint(self.pos), self.size)

    def update(self):
        dt = delta()
        self.pos = [self.pos[0] + math.cos(self.angle) * self.speed * dt, self.pos[1] + math.sin(self.angle) * self.speed * dt]


class Bullet(Projectile):
    bulletSize = 20 #diameter, not radius
    states = {
        "idle": 0,
        "moving": 1,
        "exploding": 2
    }
    bullets = []
    def __init__(self, startPos, targetPos) -> None:
        super().__init__()
        self.setVars(Bullet.bulletSize/2, None, randint(170,250), (255,0,0), startPos)
        self.angle = math.atan2((self.startPos[1] - targetPos[1]), (self.startPos[0] - targetPos[0])) + math.pi
        self.setState("moving")
        self.particles = []
        self.initParticles()
        Bullet.bullets.append(self)
    
    # def setTarget(self, pos):
    #     self.angle = math.atan2((self.startPos[1] - pos[1]), (self.startPos[0] - pos[0])) + math.pi
    
    def initParticles(self):
        for _ in range(20):
            self.particles.append(ExplosionParticle())

    def checkState(self, state):
        if self.state == Bullet.states[state]:
            return True
        return False

    def update(self):
        if self.checkState("moving"):
            super().update()
        elif self.checkState("exploding"):
            if self.checkExplosionDone():
                self.setState("idle")
            for particle in self.particles:
                particle.update()
    
    def render(self, screen):
        if self.checkState("moving"):
            super().render(screen)
        elif self.checkState("exploding"):
            for particle in self.particles:
                particle.render(screen)
    
    def setState(self, state):
        self.state = Bullet.states[state]

    def explode(self): # TODO: check to make sure this is only run once per explosion
        self.setState("exploding")
        for particle in self.particles:
            particle.launch(self.pos)
    
    @staticmethod
    def checkAllBulletsCollision(barrierMap, player):
        for row in barrierMap:
            for tile in row:
                if tile != 0:
                    for bullet in Bullet.bullets:
                        if bullet.checkState("moving"):
                            if player.rect.colliderect(pygame.Rect(bullet.pos[0] - Bullet.bulletSize/2, bullet.pos[1] - Bullet.bulletSize/2, Bullet.bulletSize, Bullet.bulletSize)):
                                bullet.explode()
                                player.takeDamage(1)
                            elif tile.rect.colliderect(pygame.Rect(bullet.pos[0] - Bullet.bulletSize/2, bullet.pos[1] - Bullet.bulletSize/2, Bullet.bulletSize, Bullet.bulletSize)):
                                bullet.explode()

    def checkExplosionDone(self): # TODO: make this shit work
        for particle in self.particles:
            if particle.isMoving:
                return False
        return True

class ExplosionParticle(Projectile):
    def __init__(self) -> None:
        super().__init__()
        self.initParticle()
        self.numLoops = randint(1,3) # number of times it resets
        self.isMoving = False

    def initParticle(self):
        self.setVars(randint(2,5), randint(0,360), randint(10,20)*10, (0,0,randint(100,255)), self.startPos)
        self.numIterations = randint(10,20) #num times it runs before it resets.

    def launch(self, pos):
        self.isMoving = True
        self.pos = [pos[0], pos[1]]
        self.startPos = self.pos
    
    def render(self, screen):
        if self.isMoving:
            super().render(screen)

    def update(self):
        if self.isMoving:
            if self.numIterations == 0:
                if self.numLoops > 0:
                    self.initParticle()
                    self.numLoops -= 1
                else:
                    self.isMoving = False
            else:
                super().update()
                self.isMoving = (self.numLoops != 0)
                self.numIterations -= 1
