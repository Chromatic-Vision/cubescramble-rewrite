import webbrowser
import pygame
import sounddevice
import game
from assets.puzzles import puzzle
from renderer import button

from config import Config


class SettingsRenderer:
    def __init__(self, config: Config, game):

        self.config = config
        self.game = game

        self.buttons = []
        self.selected = None
        self.font_height = self.game.font1.get_height()

        ry = self.font_height + 45

        for setting_name in self.config.__annotations__:
            self.buttons.append(SettingsRenderer.SettingsButton(10, ry, 1000, self.font_height, 550, setting_name, self, self.game)) # I didn't know putting self was a existing feature
            ry += self.font_height + 5

        self.help_button = button.SimpleButton(self.game.screen.get_size()[0] - 65, 10, 50, 50, "?", (17, 7), self.game, open_docs)
        self.times_button = button.SimpleButton(10, self.config.__annotations__.__len__() * (self.font_height + 5) + 45 + 45, 180, 50,
                                                          "Times...", (17, 7), self.game, self.switch_to_times_gui)


    def update(self, events: list[pygame.event.Event]):
        for event in events:

            # if event.type == pygame.MOUSEWHEEL:
            #     if event.y > 0:
            #         for b in self.buttons:
            #             b.y += 5
            #     elif event.y < 0:
            #         for b in self.buttons:
            #             b.y -= 5

            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.help_button.button_rect.collidepoint(event.pos):
                    self.help_button.on_click()

                if self.times_button.button_rect.collidepoint(event.pos):
                    self.times_button.on_click()

                for b in self.buttons:
                    if b.button_rect.collidepoint(event.pos):

                        self.selected = b.setting_name

                        if self.selected == "current_event":

                            index = puzzle.PUZZLES.index(self.config.__dict__[self.selected]) + 1

                            self.config.__dict__[self.selected] = puzzle.PUZZLES[index if index < len(puzzle.PUZZLES) else 0]

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

                    if not self.selected == "current_event":
                        self.config.__dict__[self.selected] += event.text

            elif event.type == pygame.KEYDOWN:

                # if event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                #     if self.selected is not None and pygame.scrap.get(pygame.SCRAP_TEXT) is not None:
                #         if type(self.config.__dict__[self.selected]) == str:
                #             with open("broken_text.bin", "w") as f:
                #                 f.write(pygame.scrap.get("text/plain;charset=utf-8").decode())
                #                 f.close()
                #             self.config.__dict__[self.selected] += (pygame.scrap.get("text/plain;charset=utf08").decode())

                if event.key == pygame.K_RETURN:
                    if self.selected is not None:
                        self.selected = None

                if event.key == pygame.K_BACKSPACE:
                    if self.selected is None:
                        continue

                    if type(self.config.__dict__[self.selected]) == str:

                        if not self.selected == "current_event":
                            if event.mod & pygame.KMOD_CTRL:
                                self.config.__dict__[self.selected] = ""
                            else:
                                self.config.__dict__[self.selected] = self.config.__dict__[self.selected][:-1]

                    if type(self.config.__dict__[self.selected]) == int:
                        self.config.__dict__[self.selected] = 0

                    if type(self.config.__dict__[self.selected]) == list:
                        self.config.__dict__[self.selected] = []

                if event.key == pygame.K_RIGHT:
                    if self.selected is None:
                        continue

                    if type(self.config.__dict__[self.selected]) == int:
                        self.config.__dict__[self.selected] += 1
                elif event.key == pygame.K_LEFT:
                    if self.selected is None:
                        continue

                    if type(self.config.__dict__[self.selected]) == int:
                        self.config.__dict__[self.selected] -= 1

    def draw(self, screen: pygame.Surface):

        self.game.draw_string(self.game.font1, "Settings", (10, 5))

        self.help_button.update_state()
        self.help_button.draw()

        self.times_button.update_state()
        self.times_button.draw()

        for b in self.buttons:
            b.update(b.setting_name)
            b.draw()

    def switch_to_times_gui(self):
        self.game.state = "times"
        game.update_mouse(True)

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
                # TODO: checkbox
                if self.setting:
                    string = 'true'
                else:
                    string = 'false'

                self.game.draw_string(self.game.font1, string, (self.bx, self.y), background_color=b)
            elif self.setting_type == int:
                if self.setting_name == "device_num":

                    r = "Invalid device"

                    try:
                        r = str(sounddevice.query_devices()[self.setting]["name"])
                    except:
                        pass

                    self.game.draw_string(self.game.font1, str(self.setting) + ": " + r, (self.bx, self.y), background_color=b)
                else:
                    self.game.draw_string(self.game.font1, str(self.setting), (self.bx, self.y), background_color=b)
            elif self.setting_type == list:
                self.game.draw_string(self.game.font1, str(self.setting), (self.bx, self.y), background_color=b)
            else:
                # assert False, f"unimplemented type '{setting_type}'"
                pass

def open_docs():
    webbrowser.open("https://github.com/Chromatic-Vision/cubescramble-rewrite/blob/main/DOCS.md")