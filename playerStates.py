# from world import *
from projectile import *

# world = World()

class StateGenerator:
    @staticmethod
    def setState(state: str, player):
        if state == "moving":
            return MoveState(player)
        elif state == "idle":
            return IdleState(player)
        elif state == "attacking":
            return AttackState(player)
        

class State:
    def __init__(self, player) -> None:
        self.animation = None
        self.frameFrq = 1000
        self.player = player
        pygame.time.set_timer(pygame.USEREVENT, self.frameFrq)
        self.currentFrame = 0
    
    def render(self, screen, pos):
        if self.animation != None:
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.player.currentState = StateGenerator.setState("attacking", self.player)
                if event.key == pygame.K_1:
                    self.player.setWeapon("mace")
                if event.key == pygame.K_2:
                    self.player.setWeapon("staff")
                if event.key == pygame.K_3:
                    self.player.setWeapon("gun")
            

class IdleState(State):
    def __init__(self, player) -> None:
        super().__init__(player)
        # self.animation = [pygame.Surface((50,50)), pygame.Surface((50,50)), pygame.Surface((50,50))]
        # self.animation[0].fill((255,0,0))
        # self.animation[1].fill((0,255,0))
        # self.animation[2].fill((0,0,255))
        self.animations = {
            "left" : [
                pygame.transform.scale(pygame.image.load("assets/player/left_idle_1.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/left_idle_2.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/left_idle_1.png"), (64, 120))
            ],
            "right" : [
                pygame.transform.scale(pygame.image.load("assets/player/right_idle_1.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/right_idle_2.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/right_idle_1.png"), (64, 120))
            ],
            "front" : [
                pygame.transform.scale(pygame.image.load("assets/player/front_idle_1.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/front_idle_2.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/front_idle_1.png"), (64, 120))
            ],
        }
        self.animation = self.animations[self.player.lastDirectionFaced]
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                    self.player.currentState = StateGenerator.setState("moving", self.player)

class MoveState(State):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.animations = {
            "up" : [
                pygame.transform.scale(pygame.image.load("assets/player/back_1.png"), (64, 120)), 
                pygame.transform.scale(pygame.image.load("assets/player/back_2.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/back_3.png"), (64, 120)), 
                pygame.transform.scale(pygame.image.load("assets/player/back_2.png"), (64, 120)), 
                pygame.transform.scale(pygame.image.load("assets/player/back_1.png"), (64, 120)), 
                pygame.transform.scale(pygame.image.load("assets/player/back_4.png"), (64, 120)), 
                pygame.transform.scale(pygame.image.load("assets/player/back_5.png"), (64, 120)), 
                pygame.transform.scale(pygame.image.load("assets/player/back_4.png"), (64, 120))
            ],
            "down" : [
                pygame.transform.scale(pygame.image.load("assets/player/front_1.png"), (64, 120)), 
                pygame.transform.scale(pygame.image.load("assets/player/front_2.png"), (64, 120)), 
                pygame.transform.scale(pygame.image.load("assets/player/front_3.png"), (64, 120)), 
                pygame.transform.scale(pygame.image.load("assets/player/front_2.png"), (64, 120)), 
                pygame.transform.scale(pygame.image.load("assets/player/front_1.png"), (64, 120)), 
                pygame.transform.scale(pygame.image.load("assets/player/front_4.png"), (64, 120)), 
                pygame.transform.scale(pygame.image.load("assets/player/front_5.png"), (64, 120)), 
                pygame.transform.scale(pygame.image.load("assets/player/front_4.png"), (64, 120))
            ],
            "left" : [
                pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player/side_1.png"), True, False), (64, 120)), 
                pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player/side_2.png"), True, False), (64, 120)), 
                pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player/side_3.png"), True, False), (64, 120)), 
                pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player/side_2.png"), True, False), (64, 120)), 
                pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player/side_1.png"), True, False), (64, 120)),
                pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player/side_4.png"), True, False), (64, 120)),
                pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player/side_5.png"), True, False), (64, 120)),
                pygame.transform.scale(pygame.transform.flip(pygame.image.load("assets/player/side_4.png"), True, False), (64, 120))
            ],
            "right" : [
                pygame.transform.scale(pygame.image.load("assets/player/side_1.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/side_2.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/side_3.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/side_2.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/side_1.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/side_4.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/side_5.png"), (64, 120)),
                pygame.transform.scale(pygame.image.load("assets/player/side_4.png"), (64, 120))
            ]
        }
        self.frameFrq = 100
        pygame.time.set_timer(pygame.USEREVENT, self.frameFrq)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.animation = self.animations["up"]
        elif keys[pygame.K_a]:
            self.animation = self.animations["left"]
        elif keys[pygame.K_s]:
            self.animation = self.animations["down"]
        elif keys[pygame.K_d]:
            self.animation = self.animations["right"]
        
    def handleInput(self, events, barrierMap):
        super().handleInput(events)
        dt = delta()
        keys = pygame.key.get_pressed()

        if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
            if self.animation == self.animations["left"]:
                self.player.lastDirectionFaced = "left"
            elif self.animation == self.animations["right"]:
                self.player.lastDirectionFaced = "right"
            else:
                self.player.lastDirectionFaced = "front"
            self.player.currentState = StateGenerator.setState("idle", self.player)

        if keys[pygame.K_a]:
            rect = self.player.handleBarrierCollision(barrierMap, pygame.Rect(self.player.rect.x - self.player.speed*dt, self.player.rect.y, self.player.rect.width, self.player.rect.height))
            if rect == None:
                self.player.pos[0] -= self.player.speed * dt
            else: 
                self.player.pos[0] -= (self.player.pos[0] - rect.right) * dt

        if keys[pygame.K_d]:
            rect = self.player.handleBarrierCollision(barrierMap, pygame.Rect(self.player.rect.x + self.player.speed*dt, self.player.rect.y, self.player.rect.width, self.player.rect.height))
            if rect == None:
                self.player.pos[0] += self.player.speed * dt
            else:
                self.player.pos[0] += (rect.left - self.player.rect.right) * dt

        if keys[pygame.K_w]:
            rect = self.player.handleBarrierCollision(barrierMap, pygame.Rect(self.player.rect.x, self.player.rect.y - self.player.speed*dt, self.player.rect.width, self.player.rect.height))
            if rect == None:
                self.player.pos[1] -= self.player.speed * dt
            else:
                self.player.pos[1] -= (self.player.rect.top - rect.bottom) * dt

        if keys[pygame.K_s]:
            rect = self.player.handleBarrierCollision(barrierMap, pygame.Rect(self.player.rect.x, self.player.rect.y + self.player.speed * dt, self.player.rect.width, self.player.rect.height))
            if rect == None:
                self.player.pos[1] += self.player.speed * dt
            else:
                self.player.pos[1] += (rect.top - self.player.rect.bottom) * dt
        
        if self.animation != None:
            if self.animation == self.animations["up"]:
                if keys[pygame.K_s]:
                    self.animation = self.animations["down"]
                if not keys[pygame.K_w]:
                    if keys[pygame.K_a]:
                        self.animation = self.animations["left"]
                    elif keys[pygame.K_d]:
                        self.animation = self.animations["right"]
            
            elif self.animation == self.animations["down"]:
                if keys[pygame.K_w]:
                    self.animation = self.animations["up"]
                if not keys[pygame.K_s]:
                    if keys[pygame.K_a]:
                        self.animation = self.animations["left"]
                    elif keys[pygame.K_d]:
                        self.animation = self.animations["right"]
            
            if self.animation == self.animations["left"]:
                if keys[pygame.K_d]:
                    self.animation = self.animations["right"]
                if not keys[pygame.K_a]:
                    if keys[pygame.K_w]:
                        self.animation = self.animations["up"]
                    elif keys[pygame.K_s]:
                        self.animation = self.animations["down"]
            
            elif self.animation == self.animations["right"]:
                if keys[pygame.K_a]:
                    self.animation = self.animations["left"]
                if not keys[pygame.K_d]:
                    if keys[pygame.K_w]:
                        self.animation = self.animations["up"]
                    elif keys[pygame.K_s]:
                        self.animation = self.animations["down"]



class AttackState(State):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.animations = {
            "mace" : [pygame.Surface((60,60)), pygame.Surface((40,40))],
            "staff" : [pygame.Surface((60,60)), pygame.Surface((40,40))],
            "gun" : [pygame.Surface((60,60)), pygame.Surface((40,40))]
        }
        self.animations["mace"][0].fill((255,0,0))
        self.animations["mace"][1].fill((255,0,0))
        self.animations["staff"][0].fill((0,255,0))
        self.animations["staff"][1].fill((0,255,0))
        self.animations["gun"][0].fill((0,0,255))
        self.animations["gun"][1].fill((0,0,255))
        self.animation = self.animations[self.player.weapon]

    def handleInput(self, events):
        super().handleInput(events)
    
    def update(self):
        if self.currentFrame == len(self.animation) - 1:
            self.player.currentState = StateGenerator.setState("moving", self.player)
            self.currentFrame = 0
    

