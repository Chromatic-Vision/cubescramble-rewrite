from typing import Union
import pygame
from pygame import gfxdraw
import requests
import io

import assets.scrambler.clock
import calcutils
import config
import timer
from renderer.particle import ParticleRenderer
from renderer.settings import SettingsRenderer


class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # weird, windows
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # weird, windows

        self.font1 = pygame.font.Font("assets/fonts/font1.ttf", 25)
        self.font2 = pygame.font.Font("assets/fonts/font1.ttf", 100)

        self.particlerenderer = ParticleRenderer(self.screen)

        self.timer = timer.Timer(self.particlerenderer)

        self.state = 'main'

        self.config = config.Config(0, "https://chromatic-vision.github.io/assets/images/forest-background.png", False, 'true')
        self.load()

        self.settings_renderer = SettingsRenderer(self.config, self)

        self.background = None
        self.background_image = None
        self.background_raw = None

        self.refresh_background()

        update_mouse(not self.config.hide_mouse)

    def refresh_background(self):

        if self.config.background_url is not None and self.background_image is None:
            # TODO: if you change the settings this should refresh
            if not self.config.background_local:
                r = requests.get(self.config.background_url)  # TODO: do in background
                print(r.status_code)
                if r.status_code != 200:
                    print('background image website did not return 200')
                    self.background = None
                    self.background_raw = None
                    self.background_image = None
                else:
                    try:
                        self.background_image = pygame.image.load(io.BytesIO(r.content))

                    except pygame.error:
                        print('background image brocken')
                        self.background = None
                        self.background_raw = None
                        self.background_image = None
            else:
                try:
                    self.background_image = pygame.image.load(self.config.background_url)
                except pygame.error:
                    self.background = None
                    self.background_raw = None
                    self.background_image = None
                    print('background image brocken')
                except FileNotFoundError:  # TODO: report errors in GUI
                    self.background = None
                    self.background_raw = None
                    self.background_image = None
                    print('image not found')
        else:
            self.background = None
            self.background_raw = None

        if self.background_image is not None:
            self.background_raw = pygame.Surface(self.background_image.get_size())
            self.background_raw.blit(self.background_image, (0, 0))

        if self.background_raw is not None:
            if self.config.background_scale == 'aspect':  # aspect scaling
                scale = self.background_raw.get_width() / self.screen.get_size()[0]
                scale = max(scale, self.background_raw.get_height() / self.screen.get_size()[1])

                self.background = pygame.transform.smoothscale(self.background_raw,
                                                          (self.background_raw.get_width() / scale,
                                                           self.background_raw.get_height() / scale))

            elif self.config.background_scale:  # full scaling
                self.background = pygame.transform.smoothscale(self.background_raw, self.screen.get_size())

            else:  # no scaling
                self.background = self.background_raw

    def update(self, events: list[pygame.event.Event]):

        for event in events:
            if event.type == pygame.VIDEORESIZE:
                self.refresh_background()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL: # switch UI

                    if self.state == 'settings':

                        self.background_image = None
                        self.refresh_background()

                        self.timer.time_history = self.config.times

                        timer.DEVICE_NUM = self.config.device_num
                        self.timer.reset(False) # update DEVICE_NUM of stackmat timer

                        update_mouse(not self.config.hide_mouse) # update mouse after done with settings

                        self.state = 'main'
                    else:
                        self.state = 'settings'

                        update_mouse(True) # make mouse visible so you can configure settings

        if self.state == 'main':
            self.timer.update(events)
        elif self.state == 'settings':
            self.settings_renderer.update(events)
        else:
            assert False, f"unknown state '{self.state}'"

    def draw(self):

        screen = self.screen
        screen.fill((0, 0, 0))

        if self.background is not None:
            screen.blit(self.background, (0, 0))

        if self.state == 'main':
            self.draw_main(screen)
        elif self.state == 'settings':
            self.settings_renderer.draw(screen)
        else:
            assert False, f"unknown state '{self.state}'"

        pygame.display.update()

    def draw_main(self, screen):

        """

        Code below is used to render the overall items on the screen.
        Adjust and modify the code however you want.

        """

        # particles, update of screen render
        if self.config.particles:
            self.particlerenderer.update()

        """

        Elements that only will be displayed if timer is inactive.

        """

        if self.timer.ready <= 0 and not self.timer.running:

            # current scramble
            self.draw_string(self.font1, self.timer.current_scramble, (
                self.screen.get_size()[0] / 2 - self.font1.size(self.timer.current_scramble)[0] / 2 - 5, 20))

            # draw scramble
            if self.config.draw_scramble:

                if self.timer.event == "clock":

                    x = self.screen.get_size()[0] - 395
                    y = self.screen.get_size()[1] - 200

                    # background
                    pygame.draw.rect(screen, (75, 75, 75), (x, y, x + 400, y + 200))

                    fx = x + 45
                    fy = y + 45

                    # clocks
                    for i in range(self.timer.clock.front.states.__len__()):
                        draw_antialias_circle(screen, (64, 77, 255), i % 3 * 55 + fx, i // 3 * 55 + fy, 23)

                    for i in range(self.timer.clock.back.states.__len__()):
                        draw_antialias_circle(screen, (155, 177, 25), i % 3 * 55 + fx + 195, i // 3 * 55 + fy, 23)

                    # pins
                    front_pins = self.timer.clock.pins
                    back_pins = assets.scrambler.clock.invert_pins(front_pins)

                    for i in range(front_pins.__len__()):

                        color = (86, 86, 25)

                        if front_pins[i]:
                            color = (255, 255, 0)

                        draw_antialias_circle(screen, color, i % 2 * 55 + fx + 28, i // 2 * 55 + fy + 28, 9)

                    for i in range(back_pins.__len__()):

                        color = (86, 86, 25)

                        if back_pins[i]:
                            color = (255, 255, 0)

                        draw_antialias_circle(screen, color, i % 2 * 55 + fx + 28 + 194, i // 2 * 55 + fy + 28, 9)

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

    def draw_string(self, font: pygame.font.Font, text, coords, color=(255, 255, 255), background_color=None):
        self.screen.blit(font.render(text, True, color, background_color), coords)

    def save(self):
        self.config.times = self.timer.time_history

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
        out += '.'
        millis = int(time % 1000)
        if millis < 100:
            out += '0'
        if millis < 10:
            out += '0'

        out += f'{millis}'

    return out

def update_mouse(visible):
    pygame.mouse.set_visible(visible)
    pygame.mouse.set_pos((pygame.mouse.get_pos()[0] - 0.0000000000069420, pygame.mouse.get_pos()[1]))

def draw_antialias_circle(surface, color, x, y, radius):
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)