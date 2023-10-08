import pygame
from config import Config


class SettingsRenderer:
    def __init__(self, config: Config, game):
        self.config = config
        self.game = game

        self.buttons = []
        self.selected = None
        self.font_height = self.game.font1.get_height()

        height = self.game.font1.get_height()
        ry = height + 25

        for setting_name in self.config.__annotations__:
            self.buttons.append(SettingsRenderer.SettingsButton(5, ry, 1000, height, 550, setting_name, self, self.game)) # I didn't know putting self was a existing feature
            ry += height + 5

    class SettingsButton:

        def __init__(self, x, y, width, height, offset, setting_name, renderer, game):
            self.renderer = renderer
            self.game = game

            self.setting_name = setting_name
            self.setting = eval(f'self.game.config.{setting_name}')
            self.setting_type = type(self.setting)

            self.x = x
            self.y = y
            self.bx = x + offset
            self.width = width
            self.height = height

            self.button_surface = pygame.Surface((self.width, self.height))
            self.button_rect = pygame.Rect(self.bx, self.y, self.width, self.height)

            self.state = "normal"
            self.fill_colors = {
                'normal': None,
                'hover': (100, 100, 100),
                'selected': (177, 177, 177)
            }

        def update(self, setting_name):
            self.setting_name = setting_name
            self.setting = eval(f'self.game.config.{setting_name}')
            self.setting_type = type(self.setting)

        def draw(self):
            s = self.game.font1.render(self.setting_name, True, (255, 255, 255))
            self.game.screen.blit(s, (self.x, self.y))

            self.state = "normal"

            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                self.state = "hover"

            if self.renderer.selected == self.setting_name:
                self.state = "selected"

            b = self.fill_colors[self.state]

            if self.setting_type == str:
                self.game.draw_string(self.game.font1, self.setting, (self.bx, self.y), background_color=b)
            elif self.setting_type == bool:
                # TODO: proper rendering
                if self.setting:
                    string = 'X'
                else:
                    string = 'O'

                self.game.draw_string(self.game.font1, string, (self.bx, self.y), background_color=b)
            elif self.setting_type == int:
                self.game.draw_string(self.game.font1, str(self.setting), (self.bx, self.y), background_color=b)
            elif self.setting_type == list:
                self.game.draw_string(self.game.font1, '-', (self.bx, self.y), background_color=b)
            else:
                # assert False, f"unimplemented type '{setting_type}'"
                pass


    def update(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:

                for b in self.buttons:
                    if b.button_rect.collidepoint(event.pos):

                        b.state = "clicked"

                        self.selected = b.setting_name

                        if type(eval(f'self.config.{self.selected}')) == bool:
                            self.config.__dict__[self.selected] = not self.config.__dict__[self.selected]
                            self.selected = None
                        break
                    else:
                        self.selected = None
                        continue

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

        self.game.draw_string(self.game.font1, "Settings", (5, 5))

        for b in self.buttons:
            b.update(b.setting_name)
            b.draw()