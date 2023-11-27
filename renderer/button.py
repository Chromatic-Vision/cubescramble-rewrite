import pygame

class SimpleButton:

    def __init__(self, x, y, width, height, text, text_offset, game, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.text_offset = text_offset

        self.game = game

        self.fill_colors = {
            'normal': (255, 255, 255),
            'hover': (100, 100, 100)
        }

        self.state = "normal"

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.action = action

    def draw(self):
        pygame.draw.rect(self.game.screen, self.fill_colors[self.state], self.button_rect,
                         0 if self.state == "hover" else 2)
        self.game.draw_string(self.game.font1, self.text, (self.x + self.text_offset[0], self.y + self.text_offset[1]))

    def update_state(self):
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            self.state = "hover"
        else:
            self.state = "normal"

    def update_pos(self, x, y):

        if x is not None:
            self.x = x
            self.button_rect.x = x

        if y is not None:
            self.y = y
            self.button_rect.y = y


    def on_click(self):
        self.action()