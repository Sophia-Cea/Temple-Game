from utils import deg2rad
from playerStates import *

world = Chunk()


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
    def __init__(self, pos) -> None:
        super().__init__()
        self.setVars(Bullet.bulletSize/2, None, randint(170,250), (255,0,0), pos)
        self.setState("idle")
        self.particles = []
        self.initParticles()
        Bullet.bullets.append(self)
    
    def setTarget(self, pos):
        self.angle = math.atan2((self.startPos[0] - pos[0]), (self.startPos[1] - pos[1]))
        self.setState("moving")
    
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
    def checkAllBulletsCollision():
        for row in world.foregroundMap:
            for tile in row:
                if tile != 0:
                    for bullet in Bullet.bullets:
                        if bullet.checkState("moving"):
                            if tile.rect.colliderect(pygame.Rect(bullet.pos[0] - Bullet.bulletSize/2, bullet.pos[1] - Bullet.bulletSize/2, Bullet.bulletSize, Bullet.bulletSize)):
                                bullet.explode()

    def checkExplosionDone(self): # TODO: make this shit work
        for particle in self.particles:
            if particle.isMoving:
                return False
        print("explosion Done")
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



'''
class ExplosionParticleOld:
    def __init__(self) -> None:
        self.startPos = [0,0]
        self.initParticle()
        self.numLoops = randint(1,3)
        self.isMoving = False
    
    def launch(self, pos):
        self.pos = [pos[0], pos[1]]
        self.startPos = [pos[0], pos[1]]
        self.isMoving = True
    
    def initParticle(self):
        self.angle = randint(0,360)
        self.size = randint(2,5)
        self.speed = randint(110,180)
        self.pos = self.startPos
        self.numIterations = randint(15,30) #num times it runs before it goes away.

    def render(self, screen):
        if self.isMoving:
            pygame.draw.circle(screen, (0,0,255), camera.projectPoint(self.pos), self.size)

    def update(self):
        dt = delta()
        if self.isMoving:
            if self.numIterations == 0:
                if self.numLoops > 0:
                    self.initParticle()
                    self.numLoops -= 1
            self.isMoving = (self.numLoops != 0)
            self.pos[0] += math.cos(deg2rad(self.angle)) * self.speed * dt
            self.pos[1] += math.sin(deg2rad(self.angle)) * self.speed * dt
            self.numIterations -= 1

class BulletOld:
    bulletSize = 20
    states = {
        "idle": 0,
        "moving": 1,
        "exploding": 2
    }
    bullets = []
    def __init__(self, pos) -> None:
        self.startPos = pos
        self.pos = pos
        self.angle = None
        self.speed = randint(170,250)
        self.state = Bullet.states["idle"]
        self.particles = []
        self.initParticles()
        Bullet.bullets.append(self)
    
    def setTarget(self, pos): # fix trig here
        self.angle = math.atan2((pos[0] - self.startPos[0]), (pos[1] - self.startPos[1]))
        self.state = Bullet.states["moving"]
    
    def initParticles(self):
        for i in range(20):
            self.particles.append(ExplosionParticle())
    
    def update(self):
        dt = delta()
        if self.state == Bullet.states["moving"]:
            self.pos = [self.pos[0] + math.cos(self.angle) * self.speed * dt, self.pos[1] + math.sin(self.angle) * self.speed * dt]
        elif self.state == Bullet.states["exploding"]:
            if self.checkExplosionDone():
                self.state = Bullet.states["idle"]
            else:
                for particle in self.particles:
                    particle.update()

    def render(self, screen):
        if self.state == Bullet.states["moving"]:
            pygame.draw.circle(screen, (255,0,0), camera.projectPoint(self.pos), Bullet.bulletSize/2)
        elif self.state == Bullet.states["exploding"]:
            for particle in self.particles:
                particle.render(screen)

    def explode(self):
        self.state = Bullet.states["exploding"]
        for particle in self.particles:
            particle.launch(self.pos)
    
    def checkExplosionDone(self):
        for particle in self.particles:
            if particle.isMoving:
                return False
        return True
    
    @staticmethod
    def checkAllBulletsCollision():
        for row in world.foregroundMap:
            for tile in row:
                for bullet in Bullet.bullets:
                    if tile != 0:
                        if bullet.state == Bullet.states["moving"]:
                            if tile.rect.colliderect(pygame.Rect(bullet.pos[0] - Bullet.bulletSize/2, bullet.pos[1] - Bullet.bulletSize/2, Bullet.bulletSize, Bullet.bulletSize)):
                                bullet.explode()

'''