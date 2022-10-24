# from entity import *
# from playerStates import * 
from world import *

world = World()

class StateManager:
    def __init__(self) -> None:
        self.queue = []

    def push(self, page):
        self.queue.append(page)
        page.onEnter()

    def pop(self):
        self.queue[len(self.queue)-1].onExit()
        self.queue.pop(len(self.queue)-1)

    def run(self, surface, events):
        self.queue[-1].update()
        if len(self.queue) > 1:
            for i in range(-2,0):
                self.queue[i].render(surface)
        else:
            self.queue[-1].render(surface)
        self.queue[-1].handleInput(events)

stateManager = StateManager()

class State:
    def __init__(self) -> None:
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def render(self, screen):
        pass

    def update(self):
        pass

    def handleInput(self, events):
        pass

class PlayState(State):
    def __init__(self) -> None:
        super().__init__()
        

    def render(self, screen):
        super().render(screen)
        screen.fill((0,0,10))
        world.render(screen)
        player.render(screen)


    def update(self):
        super().update()
        world.update()
        player.update()
        if player.health <= 0:
            stateManager.push(GameOverState())


    def handleInput(self, events):
        super().handleInput(events)
        world.handleInput(events)
        player.handleInput(events, world.getCurrentChunk().foregroundMap)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    stateManager.push(PauseState())

class MenuState(State):
    def __init__(self) -> None:
        super().__init__()
        self.texts = []
        self.buttons = []
    
    def render(self, screen):
        screen.fill((50, 0, 100))

    
    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)


class GameOverState(State):
    def __init__(self) -> None:
        super().__init__()

    def render(self, screen):
        super().render(screen)
        screen.fill((75,0,20))


class PauseState(State):
    def __init__(self) -> None:
        super().__init__()
    
    def render(self, screen):
        pygame.draw.rect(screen, (200,180,200), pygame.Rect(80, 80, WIDTH-160, HEIGHT-160))
    
    def handleInput(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    stateManager.pop()
