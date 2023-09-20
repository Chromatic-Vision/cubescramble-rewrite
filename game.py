import time
import pygame
from assets.stackmat import stackmat


DEVICE_NUM = 30  # TODO: be able to choose device number in GUI


class Game:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.font1 = pygame.font.Font("assets/fonts/font1.ttf", 25)
        self.timer = Timer()

    def update(self) -> bool:  # returns True if the program should continue updating

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_r:
                    self.timer.reset()
                if event.key == pygame.K_SPACE:
                    self.timer.stop()
                if event.key == pygame.K_s:
                    self.timer.timing_method = 1
                    self.timer.reset()
            elif event.type == pygame.QUIT:
                return False

        self.timer.update()

        return True

    def draw(self):

        screen = self.screen
        screen.fill((0, 0, 0))

        self.draw_string(self.font1, "Press on s for stackmat?", (5, 5))


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


class Timer:

    def __init__(self):
        self.started_timestamp = time.time_ns()
        self.running = True
        self.ms = 0
        self.timing_method = 0  # 0 = spacebar, 1 = stackmat

        self.ready = 0

        self.stackmat = None
        self.error = None

        self.reset()

    def reset(self):
        self.started_timestamp = time.time_ns()
        self.running = True
        self.error = None

        if self.stackmat is not None:
            self.stackmat.close()

        if self.timing_method == 0:
            self.stackmat = None

        elif self.timing_method == 1:
            try:
                self.stackmat = stackmat.Stackmat(DEVICE_NUM)
            except Exception as e:
                self.error = f'Error initialising stackmat: {repr(e)}'

        else:
            assert False, f"Unknown timing method {self.timing_method}"

    def update(self):
        if not self.running:
            return

        if self.timing_method == 0:
            self.ms = round((time.time_ns() - self.started_timestamp) / 1e6)

        elif self.timing_method == 1:

            if self.stackmat is not None and self.stackmat.state is not None:
                self.ms = self.stackmat.state.time
                self.error = None

                if self.stackmat.state.state == "S":
                    self.ready = -1
                elif self.stackmat.state.state == "L" or self.stackmat.state.state == "R" or self.stackmat.state.state == "I":
                    self.ready = 0
                elif self.stackmat.state.state == "C":
                    self.ready = 1
                elif self.stackmat.state.state == "A":
                    self.ready = 2
                elif self.stackmat.state.state == " ":
                    self.ready = 3

            else:
                self.ms = -1
                if self.error is None:
                    self.error = 'No data from stackmat!'

        else:
            assert False, f"Unknown timing method {self.timing_method}"

    def stop(self):
        self.running = False
