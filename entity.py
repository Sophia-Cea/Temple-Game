from numpy import deg2rad
from projectile import *



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
            if bullet.checkState("idle"):
                bullet.setTarget(pos)
                self.readyToLaunch = False
                pygame.time.set_timer(pygame.USEREVENT + 1, self.bulletFrq)
                break


class MobileEnemy(Entity):
    def __init__(self) -> None:
        super().__init__()
    