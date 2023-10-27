import pygame
import game
from config import Config


class HistoryRenderer:
    def __init__(self, config: Config, game):
        game: game.Game
        self.config = config
        self.game = game

        self.s = pygame.Surface(self.game.screen.get_size())

    def re_render(self):
        self.s.fill((0, 0, 0))
        border = 200
        self.draw_graph(self.s,
                        self.config.times[
                          -self.config.history_draw_length if len(self.config.times) > self.config.history_draw_length else None:
                        ],
                        (border, border, self.s.get_width() - border * 2, self.s.get_height() - border * 2))

    def update(self, events: list[pygame.event.Event]):
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.s, (0, 0))

    def draw_graph(self, screen: pygame.Surface, times: list[int], rect: tuple[int, int, int, int]):
        ox = rect[0]
        oy = rect[1]
        old_x = None
        old_y = None
        width = rect[2]
        height = rect[3]
        longest = max(times)
        shortest = min(times)

        pygame.draw.line(screen, (200, 200, 200), (ox, oy), (ox, oy + height), 1)
        pygame.draw.line(screen, (200, 200, 200), (ox, oy), (ox + width, oy), 1)

        s = self.game.font1.render(game.time_str(longest, True), True, (200, 200, 200))
        w = s.get_width()
        screen.blit(s, (ox - w, oy))

        y = round((longest - shortest) / longest * height)
        pygame.draw.line(screen, (200, 200, 200), (ox, oy + y), (ox + width, oy + y), 1)

        s = self.game.font1.render(game.time_str(shortest, True), True, (200, 200, 200))
        w = s.get_width()
        screen.blit(s, (ox - w, oy + y))

        for i, time in enumerate(times):
            x = round(i / len(times) * width)
            y = round((longest - time) / longest * height)
            if old_y is not None:
                pygame.draw.aaline(screen, (255, 255, 255),
                                 (ox + old_x, oy + old_y),
                                 (ox + x, oy + y))
            # pygame.draw.circle(screen, (255, 255, 255), (ox + x, oy + y), 4)
            game.draw_antialias_circle(screen, (255, 255, 255), ox + x, oy + y, 4)
            old_x = x
            old_y = y
