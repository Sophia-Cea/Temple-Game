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
        self.queue[len(self.queue)-1].update()
        self.queue[len(self.queue)-1].render(surface)
        self.queue[len(self.queue)-1].handleInput(events)

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


    def handleInput(self, events):
        super().handleInput(events)
        world.handleInput(events)
        player.handleInput(events, world.getCurrentChunk().foregroundMap)

class MenuState(State):
    def __init__(self) -> None:
        super().__init__()