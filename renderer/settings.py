import pygame
from config import Config


class SettingsRenderer:
    def __init__(self, config: Config, game):
        self.config = config
        self.game = game

        self.selected = None
        self.font_height = self.game.font1.get_height()

    def update(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                i = event.pos[1] // self.font_height
                settings = list(self.config.__annotations__.keys())

                if i < len(settings):
                    self.selected = settings[i]

                    if type(eval(f'self.config.{self.selected}')) == bool:
                        self.config.__dict__[self.selected] = not self.config.__dict__[self.selected]
                        self.selected = None
                else:
                    self.selected = None
            elif event.type == pygame.TEXTINPUT:
                if self.selected is None:
                    continue

                if type(self.config.__dict__[self.selected]) == str:
                    self.config.__dict__[self.selected] += event.text
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.selected is None:
                        continue

                    if type(self.config.__dict__[self.selected]) == str:
                        self.config.__dict__[self.selected] = self.config.__dict__[self.selected][:-1]

    def draw(self, screen: pygame.Surface):
        x = 500
        y = 0
        for setting_name in self.config.__annotations__:
            setting = eval(f'self.config.{setting_name}')
            setting_type = type(setting)

            s = self.game.font1.render(setting_name, True, (255, 255, 255))
            screen.blit(s, (0, y))

            b = None
            if self.selected == setting_name:
                b = (0, 0, 0)

            if setting_type == str:
                self.game.draw_string(self.game.font1, setting, (x, y), background_color=b)
            elif setting_type == bool:
                # TODO: proper rendering
                if setting:
                    string = 'X'
                else:
                    string = 'O'

                self.game.draw_string(self.game.font1, string, (x, y), background_color=b)
            elif setting_type == int:
                self.game.draw_string(self.game.font1, str(setting), (x, y), background_color=b)
            elif setting_type == list:
                self.game.draw_string(self.game.font1, 'X', (x, y), background_color=b)
            else:
                # assert False, f"unimplemented type '{setting_type}'"
                pass

            y += s.get_height()
