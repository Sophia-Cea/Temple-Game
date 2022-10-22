from entity import *



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
        self.player = Player()
        self.enemies = [FixedEnemy((10,10), 1000), FixedEnemy((1,1), 5000), FixedEnemy((10,20), 500), FixedEnemy((1,10), 1000)]

    def render(self, screen):
        super().render(screen)
        screen.fill((0,0,10))
        world.render(screen)
        self.player.render(screen)
        for enemy in self.enemies:
            enemy.render(screen)


    def update(self):
        super().update()
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
            if enemy.readyToLaunch:
                if measureDistance(enemy.pos, self.player.pos) <= 200:
                    enemy.launchBullet(self.player.rect.center)
        Bullet.checkAllBulletsCollision()


    def handleInput(self, events):
        super().handleInput(events)
        self.player.handleInput(events)
        for enemy in self.enemies:
            enemy.handleInput(events)


