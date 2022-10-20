from numpy import deg2rad
from playerStates import *


world = Chunk()

class Entity:
    def __init__(self) -> None:
        self.pos = [950, 800]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 50,50)
        self.surface = pygame.Surface(self.rect.size)
        self.surface.fill((255,0,255))

    def render(self, screen):
        r = self.rect.move(-camera.xOffset + WIDTH/2, -camera.yOffest + HEIGHT/2)
        screen.blit(self.surface, (r.x, r.y))
        
    def update(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def handleBarrierCollision(self, entityRect: pygame.Rect=None):
        if entityRect == None:
            entityRect = self.rect
        for i in range(len(world.foregroundMap)):
            for j in range(len(world.foregroundMap[i])):
                if world.foregroundMap[i][j] != 0:
                    rect = (world.foregroundMap[i][j].rect)
                    if entityRect.colliderect(rect):
                        return rect
        return None


class Player(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.lives = 3
        self.speed = 300
        self.surface = pygame.Surface(self.rect.size)
        self.surface.fill((255,0,0))
        self.states = {
            "idle" : IdleState(self),
            "moving" : MoveState(self)
        }
        self.currentState = self.states["idle"]

    def render(self, screen):
        super().render(screen)
        self.currentState.render(screen, self.rect.move(-camera.xOffset + WIDTH/2, -camera.yOffest + HEIGHT/2))

    def update(self):
        super().update()
        camera.lerp_to(self.rect.centerx, self.rect.centery, 0.05)
        self.currentState.update()
        

    def handleInput(self, events):
        self.currentState.handleInput(events)

class FixedEnemy(Entity):
    size = Tile.tileSize
    def __init__(self, pos) -> None:
        super().__init__()
        # pos is given in the form of a position in the grid
        self.pos = [pos[0]*Tile.tileSize, pos[1]*Tile.tileSize]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], FixedEnemy.size, FixedEnemy.size)
        self.bullets = []
        self.bulletFrq = 3000
        for i in range(5):
            self.bullets.append(Bullet(self.rect.center))
        pygame.time.set_timer(pygame.USEREVENT + 1, self.bulletFrq)
        self.readyToLaunch = False

    def update(self):
        super().update()
        for bullet in self.bullets:
            bullet.update()

    def render(self, screen):
        for bullet in self.bullets:
            bullet.render(screen)
        super().render(screen)
    
    def handleInput(self, events):
        for event in events:
            if event.type == pygame.USEREVENT + 1:
                self.readyToLaunch = True
    
    def launchBullet(self, pos):
        for bullet in self.bullets:
            if bullet.state == Bullet.states["idle"]:
                bullet.setTarget(pos)
                self.readyToLaunch = False
                pygame.time.set_timer(pygame.USEREVENT + 1, self.bulletFrq)
                break


class MobileEnemy(Entity):
    def __init__(self) -> None:
        super().__init__()
    

class Bullet:
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
        print(self.angle)
        self.state = Bullet.states["moving"]
    
    def initParticles(self):
        for i in range(20):
            self.particles.append(ExplosionParticle())
    
    def update(self):
        dt = delta()
        if self.state == Bullet.states["moving"]:
            self.pos = (self.pos[0] + math.cos(self.angle) * self.speed * dt, self.pos[1] + math.sin(self.angle) * self.speed * dt)
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

class ExplosionParticle:
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