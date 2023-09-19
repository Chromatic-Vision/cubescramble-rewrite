import time
import pygame


class Game:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.font1 = pygame.font.Font("assets/fonts/font1.ttf", 25)
        #self.stackmat = Stackmat(30)
        self.timer = Timer()

    def update(self) -> bool: # returns bool if the program should continue updating

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_r:
                    self.timer.reset()
                if event.key == pygame.K_SPACE:
                    self.timer.stop()

        if self.timer.running:
            self.timer.ms = (int(str(time.time_ns() - self.timer.started_timestamp)[:-6]) if str(time.time_ns() - self.timer.started_timestamp).__len__() > 6 else 0)

        return True

    def draw(self):

        screen = self.screen
        screen.fill((0, 0, 0))

        self.draw_string(self.font1, "Hello, Huub!!!", (5, 5))
        self.draw_string(self.font1, f"{self.timer.ms}", (5, 40))

        pygame.display.update()

    def draw_string(self, font: pygame.font.Font, text, coords, color=(255, 255, 255)):
        self.screen.blit(font.render(text, True, color), coords)

class Timer:

    def __init__(self):
        self.started_timestamp = time.time_ns()
        self.running = True
        self.ms = 0
        self.timing_method = 0 # 0 = spacebar, 1 = stackmat

    def reset(self):
        self.started_timestamp = time.time_ns()
        self.running = True

    def stop(self):
        self.running = False