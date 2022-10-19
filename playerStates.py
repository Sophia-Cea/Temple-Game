from world import *

class State:
    def __init__(self, player) -> None:
        self.animation = None
        self.frameFrq = 1000
        self.player = player
        pygame.time.set_timer(pygame.USEREVENT, self.frameFrq)
        self.currentFrame = 0
    
    def render(self, screen, pos):
        screen.blit(self.animation[self.currentFrame], pos)

    def update(self):
        pass

    def handleInput(self, events):
        for event in events:
            if event.type == pygame.USEREVENT:
                if self.currentFrame < len(self.animation)-1:
                    self.currentFrame += 1
                else:
                    self.currentFrame = 0


class IdleState(State):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.animation = [pygame.Surface((50,50)), pygame.Surface((50,50)), pygame.Surface((50,50))]
        self.animation[0].fill((255,0,0))
        self.animation[1].fill((0,255,0))
        self.animation[2].fill((0,0,255))
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.player.currentState = self.player.states["moving"]


class MoveState(State):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.animation = [pygame.Surface((50,50)), pygame.Surface((50,50))]
        self.frameFrq = 200
        pygame.time.set_timer(pygame.USEREVENT, self.frameFrq)
        self.animation[0].fill((255,255,255))
        self.animation[1].fill((0,0,0))
        
    
    def handleInput(self, events):
        super().handleInput(events)
        dt = delta()
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.player.currentState = self.player.states["idle"]

        if keys[pygame.K_LEFT]:
            rect = self.player.handleBarrierCollision(pygame.Rect(self.player.rect.x - self.player.speed*dt, self.player.rect.y, self.player.rect.width, self.player.rect.height))
            if rect == None:
                self.player.pos[0] -= self.player.speed * dt
            else: 
                self.player.pos[0] -= (self.player.pos[0] - rect.right) * dt

        if keys[pygame.K_RIGHT]:
            rect = self.player.handleBarrierCollision(pygame.Rect(self.player.rect.x + self.player.speed*dt, self.player.rect.y, self.player.rect.width, self.player.rect.height))
            if rect == None:
                self.player.pos[0] += self.player.speed * dt
            else:
                self.player.pos[0] += (rect.left - self.player.rect.right) * dt

        if keys[pygame.K_UP]:
            rect = self.player.handleBarrierCollision(pygame.Rect(self.player.rect.x, self.player.rect.y - self.player.speed*dt, self.player.rect.width, self.player.rect.height))
            if rect == None:
                self.player.pos[1] -= self.player.speed * dt
            else:
                self.player.pos[1] -= (self.player.rect.top - rect.bottom) * dt

        if keys[pygame.K_DOWN]:
            rect = self.player.handleBarrierCollision(pygame.Rect(self.player.rect.x, self.player.rect.y + self.player.speed * dt, self.player.rect.width, self.player.rect.height))
            if rect == None:
                self.player.pos[1] += self.player.speed * dt
            else:
                self.player.pos[1] += (rect.top - self.player.rect.bottom) * dt
        
        if keys[pygame.K_RETURN]:
            print("Self.pos = ", self.player.pos)
            print(f"Camera = [{camera.xOffset}, {camera.yOffest}]")


    