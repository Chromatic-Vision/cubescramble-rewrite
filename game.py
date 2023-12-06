from typing import Union
import pygame
import pygame.gfxdraw
import requests
import io
from math import sin, cos, radians, atan2, pi

import assets.puzzles.abstract_puzzle
import config
import crf
import timer
from renderer.particle import ParticleRenderer
from renderer.settings import SettingsRenderer
from renderer.history import HistoryRenderer
from renderer.times import TimesManagerRenderer


class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # weird, windows
        self.screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)  # weird, windows

        self.font1 = pygame.font.Font("assets/fonts/font1.ttf", 25)
        self.font2 = pygame.font.Font("assets/fonts/font1.ttf", 100)

        initcheck()

        self.state = 'main'

        self.config = config.Config(1, "example.png", True, 'true', 'clock')
        self.load()

        self.timer = timer.Timer(self)
        self.time_stats = timer.TimeStats()

        self.particle_renderer = ParticleRenderer(self.screen)
        self.settings_renderer = SettingsRenderer(self.config, self)
        self.history_renderer = HistoryRenderer(self.config, self)
        self.times_manager_renderer = TimesManagerRenderer(self.config, self)

        self.background = None
        self.background_image = None
        self.background_raw = None

        self.refresh_background()
        self.timer.refresh_stats()

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
                if event.key == pygame.K_s and event.mod & pygame.KMOD_CTRL:  # switch UI

                    if self.state == 'settings':

                        self.background_image = None
                        self.refresh_background()

                        self.timer.refresh_stats()

                        timer.DEVICE_NUM = self.config.device_num
                        self.timer.event = self.config.current_event
                        self.timer.rescramble()
                        self.timer.reset(False)  # update DEVICE_NUM of stackmat timer

                        update_mouse(not self.config.hide_mouse)  # update mouse after done with settings

                        self.state = 'main'
                    else:
                        self.state = 'settings'

                        update_mouse(True)  # make mouse visible so you can configure settings
                elif event.key == pygame.K_h and event.mod & pygame.KMOD_CTRL:
                    if self.state == 'main':
                        self.history_renderer.re_render()
                        self.state = 'history'
                    else:
                        self.state = 'main'
                elif event.key == pygame.K_t and event.mod & pygame.KMOD_CTRL:
                    if self.state == 'main':
                        self.times_manager_renderer.refresh()
                        self.state = 'times'
                        update_mouse(True)
                    else:
                        self.timer.refresh_stats()
                        update_mouse(not self.config.hide_mouse)
                        self.state = 'main'

        if self.state == 'main':
            self.timer.update(events)
        elif self.state == 'settings':
            self.settings_renderer.update(events)
        elif self.state == 'history':
            self.history_renderer.update(events)
        elif self.state == 'times':
            self.times_manager_renderer.update(events)
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
        elif self.state == 'history':
            self.history_renderer.draw(screen)
        elif self.state == 'times':
            self.times_manager_renderer.draw(screen)
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
            self.particle_renderer.update()

        """

        Elements that only will be displayed if timer is inactive.

        """

        if self.timer.ready <= 0 and not self.timer.running:

            # current scramble
            self.draw_string(self.font1, self.timer.current_scramble, (
                self.screen.get_size()[0] / 2 - self.font1.size(self.timer.current_scramble)[0] / 2 - 5, 20))

            # draw scramble
            if self.config.draw_scramble:
                # TODO: make scrambler responsible for drawing itself
                # TODO: render pyraminx

                self.timer.puzzle.renderer.render(self.screen, None)

                # pyraminx
                #     x = self.screen.get_size()[0] - 500
                #     y = self.screen.get_size()[1] - 250
                #
                #     # background
                #     pygame.draw.rect(screen, (75, 75, 75), (x, y, x + 500, y + 250))


            # time stats
            reversed_time_stats_list = self.time_stats.stats[::-1]

            tx = 0

            for stat in reversed_time_stats_list:
                self.draw_string(self.font1, f"{stat.type}{stat.amount}: {time_str(stat.ms, long=True)}", (5, screen.get_size()[1] - 40 - tx))
                tx += 25

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

    def on_timer_start(self):
        self.particle_renderer.clear()

    def on_timer_stop(self):
        self.particle_renderer.refresh(70)


    def draw_string(self, font: pygame.font.Font, text, coords, color=(255, 255, 255), background_color=None):
        self.screen.blit(font.render(text, True, color, background_color), coords)

    def save(self):
        self.config.save()

    def load(self):
        try:
            self.config.load()
        except FileNotFoundError:
            pass

        timer.DEVICE_NUM = self.config.device_num


def time_str(time: Union[int, str], long: bool = False) -> str:

    if type(time) == str:
        return time

    if time == -1:
        return "-"

    if time == -2:
        return "DNF"

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
    pygame.gfxdraw.aacircle(surface, round(x), round(y), radius, color)
    pygame.gfxdraw.filled_circle(surface, round(x), round(y), radius, color)


def draw_aa_pie(surface, color, from_, to, radius):
    draw_antialias_circle(surface, color, from_[0], from_[1], radius)

    direction = atan2(from_[0] - to[0], from_[1] - to[1])

    args = [
        surface,
        round(from_[0] + sin(direction + pi / 2) * radius),
        round(from_[1] + cos(direction + pi / 2) * radius),

        round(from_[0] + sin(direction - pi / 2) * radius),
        round(from_[1] + cos(direction - pi / 2) * radius),

        round(to[0]), round(to[1]), color
    ]
    pygame.gfxdraw.filled_trigon(*args)
    pygame.gfxdraw.aatrigon(*args)


def initcheck():
    crf.CrfHandler().check_file()