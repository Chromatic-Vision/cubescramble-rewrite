import pygame.surface
import game
from config import Config
from renderer import button


class TimesManagerRenderer:

    def __init__(self, config: Config, game):
        game: game.Game
        self.config = config
        self.game = game

        self.time_buttons = []

        ry = 45

        for time in self.config.times:
            self.time_buttons.append(TimesManagerRenderer.TimeButton(10, ry, time, self.game))
            ry += 55

    def draw(self, screen):
        for tb in self.time_buttons:
            tb.draw()

    def update(self, events: list[pygame.event.Event]):

        for event in events:
            pass

        for tb in self.time_buttons:
            tb.update()

    class TimeButton:

        def __init__(self, x, y, time, game):
            self.x = x
            self.y = y

            self.game = game

            self.time = time

            self.buttons = [
                button.SimpleButton(self.game.screen.get_size()[0] - 300, self.y, 50, 50, "+2", (10, 7), self.game, self.add_plus_2),
                button.SimpleButton(self.game.screen.get_size()[0] - 240, self.y, 64, 50, "DNF", (10, 7), self.game, self.add_plus_2)
            ]

        def add_plus_2(self):
            self.time += 2
            print(self.time)

        def draw(self):

            self.game.draw_string(self.game.font1, game.time_str(self.time, long=True), (self.x + 15, self.y))

            for b in self.buttons:
                b.draw()

        def update(self):
            for b in self.buttons:
                b.update_state()