from typing import Union
import pygame

import calcutils
import config
import timer


class Game:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        self.font1 = pygame.font.Font("assets/fonts/font1.ttf", 25)
        self.timer = timer.Timer()

        self.config = config.Config(0)
        self.load()

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

        """
        
        Code below is used to render the overall items on the screen.  
        Adjust and modify the code however you want.
        
        """

        # ao5
        ao5 = calcutils.get_average_of(self.timer.time_history, 5)
        if ao5 == -1:
            ao5 = '-'
        ao5 = time_str(ao5, True)
        self.draw_string(self.font1, f"ao5: {ao5}", (5, screen.get_size()[1] - 65))

        # ao12
        ao12 = calcutils.get_average_of(self.timer.time_history, 12)
        if ao12 == -1:
            ao12 = '-'
        ao12 = time_str(ao12, True)
        self.draw_string(self.font1, f"ao12: {ao12}", (5, screen.get_size()[1] - 40))

        """
        
        End
        
        """

        if self.timer.ready <= 0 and not self.timer.running:
            self.draw_string(self.font1, "Press on s for stackmat?", (5, 5))

        c = (255, 255, 255)
        long = not self.timer.running
        if self.timer.ready == 1:
            c = (255, 0, 0)
            long = False
        elif self.timer.ready == 2:
            c = (0, 255, 0)
            long = False

        s = time_str(int(self.timer.ms), long)
        if self.timer.error is not None:
            c = (255, 0, 0)
            s = self.timer.error
        self.draw_string(self.font1, s, (5, 40), color=c)

        pygame.display.update()

    def draw_string(self, font: pygame.font.Font, text, coords, color=(255, 255, 255)):
        self.screen.blit(font.render(text, True, color), coords)

    def save(self):
        self.config.times = self.timer.time_history
        self.config.device_num = timer.DEVICE_NUM

        self.config.save()

    def load(self):
        try:
            self.config.load()
        except FileNotFoundError:
            pass
        self.timer.time_history = self.config.times
        timer.DEVICE_NUM = self.config.device_num


def time_str(time: Union[int, str], long: bool = False) -> str:
    if type(time) == str:
        return time

    seconds = time // 1000 % 60
    out = ''
    if time // 60000 > 0:
        out += f'{int(time // 60000)}:'
        if seconds < 10:
            out += '0'

    out += f'{int(seconds)}'
    if long:
        out += f'.{int(time % 1000)}'

    return out
