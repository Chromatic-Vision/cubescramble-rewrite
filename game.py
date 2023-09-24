import pygame
import timer


class Game:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.font1 = pygame.font.Font("assets/fonts/font1.ttf", 25)
        self.timer = timer.Timer()

    def update(self) -> bool:  # returns True if the program should continue updating

        events = pygame.event.get()

        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

            elif event.type == pygame.QUIT:
                return False

        self.timer.update(events)

        return True

    def draw(self):

        screen = self.screen
        screen.fill((0, 0, 0))

        if self.timer.ready <= 0 and not self.timer.running:
            self.draw_string(self.font1, "Press on s for stackmat?", (5, 5))

        self.draw_string(self.font1, f"Running: {self.timer.running}", (5, 140))

        c = (255, 255, 255)
        if self.timer.ready == 1:
            c = (255, 0, 0)
        elif self.timer.ready == 2:
            c = (0, 255, 0)

        s = repr(self.timer.ms)
        if self.timer.error is not None:
            c = (255, 0, 0)
            s = self.timer.error
        self.draw_string(self.font1, s, (5, 40), color=c)

        pygame.display.update()

    def draw_string(self, font: pygame.font.Font, text, coords, color=(255, 255, 255)):
        self.screen.blit(font.render(text, True, color), coords)
