from attr import s
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
        player.handleInput(events, world.getCurrentChunk().getCurrentRoom().foregroundTiles)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    stateManager.push(PauseState())

class MenuState(State):
    def __init__(self) -> None:
        super().__init__()
        self.texts = [Text("Curse of Pupper", "title", (255,250,235), (50,10), True)]
        self.buttons = [Button("New Game", pygame.Rect(35,50, 30,12), 35, [255,255,255], [220,170,200], [120,0,50])]
        self.bg = pygame.transform.scale(pygame.image.load("assets/other/menu_bg.png"), (WIDTH,HEIGHT))
    
    def render(self, screen):
        # screen.fill((50, 0, 100))
        screen.blit(self.bg, (0,0))
        for text in self.texts: 
            text.draw(screen)
        for button in self.buttons:
            button.draw(screen)

    
    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for i in range(len(self.buttons)):
                    if self.buttons[i].checkMouseOver(pos):
                        if i == 0:
                            stateManager.push(PlayState())
                            # stateManager.push(DialogueState(["yee", "yeeeee", "meep"]))


class GameOverState(State):
    def __init__(self) -> None:
        super().__init__()
        self.fadingIn = False
        self.fadingOut = True
        self.opacity = 0
        self.background = pygame.Surface((WIDTH,HEIGHT))
        self.background.fill((0,0,0))
        self.background.set_alpha(self.opacity)

    def render(self, screen):
        super().render(screen)
        if not self.fadingOut:
            screen.fill((75,0,20)) # TODO draw a game over screen with gold that youll never have
        if self.fadingIn or self.fadingOut:
            screen.blit(self.background, (0,0))
    
    def update(self):
        super().update()
        if self.fadingIn:
            if self.opacity > 0:
                self.opacity -= 2
            else: 
                self.fadingIn = False
            self.background.set_alpha(self.opacity)
        elif self.fadingOut:
            if self.opacity < 254:
                self.opacity += 2
            else:
                self.fadingIn = True
                self.fadingOut = False
            self.background.set_alpha(self.opacity)



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

class DialogueState(State):
    def __init__(self, texts: list) -> None:
        super().__init__()
        self.texts = []
        for text in texts:
            self.texts.append(Text(text, "paragraph", (255,255,255), (20,70), False))
        self.image = pygame.transform.scale(pygame.image.load("assets/other/textbox.png"), (700,220))
        self.index = 0
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill((0,0,0))
        self.background.set_alpha(100)
    
    def render(self, screen):
        super().render(screen)
        screen.blit(self.background, (0,0))
        screen.blit(self.image, (150, 450))
        self.texts[self.index].draw(screen)


    
    def update(self):
        super().update()
    
    def handleInput(self, events):
        super().handleInput(events)
