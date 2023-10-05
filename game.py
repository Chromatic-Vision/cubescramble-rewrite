from typing import Union
import pygame
import requests
import io
import calcutils
import config
import timer
from renderer.particle import ParticleRenderer


class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # weird, windows
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # weird, windows

        self.font1 = pygame.font.Font("assets/fonts/font1.ttf", 25)
        self.font2 = pygame.font.Font("assets/fonts/font1.ttf", 100)

        self.particlerenderer = ParticleRenderer(self.screen)

        self.timer = timer.Timer(self.particlerenderer) # TODO: move those

        self.background_url = ""

        self.config = config.Config(0, "https://snoworange420.github.io/assets/bob.png")
        self.load()

        self.background_image = None

        # get background image
        r = requests.get(self.background_url)

        if r.status_code != 200:
            print(repr(r))
        else:
            self.background_image = pygame.image.load(io.BytesIO(r.content))


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

        if self.background_image is not None:
            background_image = pygame.transform.smoothscale(self.background_image, screen.get_size())
            screen.blit(background_image, (0, 0))

        """
        
        Code below is used to render the overall items on the screen.  
        Adjust and modify the code however you want.
        
        """

        # particles
        self.particlerenderer.update()

        """
        
        Elements that only will be displayed if timer is inactive.
        
        """

        if self.timer.ready <= 0 and not self.timer.running:

            # current scramble
            self.draw_string(self.font1, self.timer.current_scramble, (self.screen.get_size()[0] / 2 - self.font1.size(self.timer.current_scramble)[0] / 2 - 5, 20))

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
        
        Elements that will be displayed all the time.
        
        """

        # time
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

        self.draw_string(self.font2, s, (self.screen.get_size()[0] / 2 - self.font2.size(s)[0] / 2 - 5,
                                         self.screen.get_size()[1] / 2 - self.font2.size(s)[1] / 2), color=c)

        """
        
        End
        
        """

        pygame.display.update()

    def draw_string(self, font: pygame.font.Font, text, coords, color=(255, 255, 255)):
        self.screen.blit(font.render(text, True, color), coords)

    def save(self):
        self.config.times = self.timer.time_history
        self.config.device_num = timer.DEVICE_NUM

        self.config.background_url = self.background_url

        self.config.save()

    def load(self):
        try:
            self.config.load()
        except FileNotFoundError:
            pass
        self.timer.time_history = self.config.times
        timer.DEVICE_NUM = self.config.device_num

        self.background_url = self.config.background_url


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
        out += '.'
        millis = int(time % 1000)
        if millis < 100:
            out += '0'
        if millis < 10:
            out += '0'

        out += f'{millis}'

    return out
