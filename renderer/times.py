import pygame.surface

import crf
import game
from config import Config
from renderer import button


class TimesManagerRenderer:

    def __init__(self, config: Config, game):
        game: game.Game
        self.config = config
        self.game = game
        self.crf_handler = crf.CrfHandler()

        self.time_buttons = []
        self.refresh()
        self.ry = 45 + 25
        self.gy = 25

    def refresh(self):

        self.time_buttons = []

        self.gy = 25
        self.ry = 45 + 25

        for time in self.crf_handler.get_all()[::-1]:
            self.time_buttons.append(TimesManagerRenderer.TimeButton(10, self.ry, time, self.game))
            self.ry += 55

    def draw(self, screen):
        if not self.time_buttons:
            self.game.draw_string(self.game.font1, "You don't have any solves completed... yet.", (self.game.screen.get_size()[0] / 2 - self.game.font1.size("You don't have any solves completed... yet.")[0] / 2, self.game.screen.get_size()[1] / 2), (255, 255, 255),
                                  background_color=None)
        else:

            self.game.draw_string(self.game.font1, "Time list", (30, self.gy), (255, 255, 255), background_color=None)

            for tb in self.time_buttons:
                tb.draw()

    def update(self, events: list[pygame.event.Event]):

        # print(self.gy)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for tb in self.time_buttons:
                    for sb in tb.buttons:
                        if sb.button_rect.collidepoint(event.pos):
                            sb.on_click()

            elif event.type == pygame.MOUSEWHEEL:

                if event.y < 0:

                    y = event.y * 10

                    for tb in self.time_buttons:
                        tb.y += y
                        tb.update_pos()

                    self.gy += y

                elif event.y > 0:

                    y = event.y * 10

                    for tb in self.time_buttons:

                        tb.y += y
                        tb.update_pos()

                    self.gy += y

            elif event.type == pygame.VIDEORESIZE:
                self.__init__(self.config, self.game)  # TODO: this seems really stupid

        for tb in self.time_buttons:
            tb.update()

    class TimeButton:

        def __init__(self, x, y, time: crf.Result, game):
            self.x = x
            self.y = y

            self.game = game

            self.time = time
            self.crf_handler = crf.CrfHandler()

            self.buttons = [
                button.SimpleButton(self.game.screen.get_size()[0] - 220, self.y, 50, 50, "+2", (10, 7), self.game, self.add_plus_2),
                button.SimpleButton(self.game.screen.get_size()[0] - 160, self.y, 64, 50, "DNF", (10, 7), self.game, self.set_dnf),
                button.SimpleButton(self.game.screen.get_size()[0] - 86, self.y, 50, 50, "R", (17, 7), self.game,self.reset_penalty)
            ]

        def add_plus_2(self):
            self.time.add_penalty("2")
            self.crf_handler.update_line(self.time)

        def set_dnf(self):
            self.time.add_penalty("DNF")
            self.crf_handler.update_line(self.time)

        def reset_penalty(self):
            self.time.add_penalty("none")
            self.crf_handler.update_line(self.time)


        def draw(self): # TODO: scramble length fix

            if self.time.penalty.isdigit():
                formatted_time_including_penalties = f"{game.time_str(self.time.time, long=True)}" + (int(int(self.time.penalty) / 2) * "+") + " "
            elif self.time.penalty == "DNF":
                formatted_time_including_penalties = f"DNF({game.time_str(self.time.time, long=True)})"
            else:
                formatted_time_including_penalties = f"{game.time_str(self.time.time, long=True)}"

            dstr = formatted_time_including_penalties + " >> " + self.time.to_string().split(" ", 2)[2]


            # self.game.draw_string(self.game.font1, f"{self.time.index}. {dstr}", (self.x + 20, self.y + 7))

            self.game.draw_string(self.game.font1, dstr, (self.x + 20, self.y + 7))

            for b in self.buttons:
                b.draw()

        def update(self):
            for b in self.buttons:
                b.update_state()

        def update_pos(self):
            for b in self.buttons:
                b.update_pos(None, self.y)