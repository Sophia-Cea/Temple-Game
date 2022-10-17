from world import *

world = World()

class Entity:
    def __init__(self) -> None:
        self.pos = [500, 350]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 50,50)
        self.surface = pygame.Surface(self.rect.size)
        self.surface.fill((255,0,255))

    def render(self, screen):
        r = self.rect.move(-camera.xOffset + WIDTH/2, -camera.yOffest + HEIGHT/2)
        screen.blit(self.surface, (r.x, r.y))
        
    def update(self):
        pass

    def handleBarrierCollision(self):
        rects = []
        for i in range(len(world.foregroundMap)):
            for j in range(len(world.foregroundMap[i])):
                rect = pygame.Rect(-camera.xOffset + j*world.tileSize, -camera.yOffest + i*world.tileSize, world.tileSize, world.tileSize)
                if world.foregroundMap[i][j] == 1 and self.rect.colliderect(rect):
                    rects.append(rect)
        return rects
                

class Player(Entity):
    def __init__(self) -> None:
        super().__init__()
        self.lives = 3
        self.speed = 3
        self.surface = pygame.Surface(self.rect.size)
        self.surface.fill((255,0,0))

    def render(self, screen):
        super().render(screen)
        pygame.draw.rect(screen, (255,0,0), self.rect.move(-camera.xOffset + WIDTH/2, -camera.yOffest + HEIGHT/2), 2)
        # screen.blit(self.surface, (-camera.xOffset + WIDTH/2, -camera.yOffest + HEIGHT/2), special_flags=pygame.BLEND_RGB_ADD)

    
    def update(self):
        super().update()
        # rect = self.handleBarrierCollision()
        # if rect != None:
        #     if self.rect.left < rect.right:
        #         self.pos[0] = rect.right - self.rect.left + 1

        #     elif self.rect.right > rect.left:
        #         self.pos[0] = self.rect.right - rect.left - 1

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        camera.lerp_to(self.rect.centerx, self.rect.centery, 0.05)


    def handleInput(self, events):
        keys = pygame.key.get_pressed()
        rects = self.handleBarrierCollision()

        if keys[pygame.K_LEFT]:
            # for rect in rects:
                self.pos[0] -= self.speed * delta

        if keys[pygame.K_RIGHT]:
            self.pos[0] += self.speed * delta

        if keys[pygame.K_UP]:
            self.pos[1] -= self.speed * delta

        if keys[pygame.K_DOWN]:
           self.pos[1] += self.speed * delta
        
        if keys[pygame.K_RETURN]:
            print("Self.pos = ", self.pos)
            print(f"Camera = [{camera.xOffset}, {camera.yOffest}]")
        # print(delta)


class Enemy(Entity):
    def __init__(self) -> None:
        super().__init__()
    
