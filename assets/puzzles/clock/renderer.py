import pygame
from assets.puzzles.abstract_puzzle_renderer import AbstractPuzzleRenderer
from assets.puzzles.clock.emulator import ClockEmulator
import game
from math import sin, cos, pi


def _invert_pins(pins):
    return [not pins[1], not pins[0], not pins[3], not pins[2]]


class ClockRenderer(AbstractPuzzleRenderer):
    def __init__(self, clock: ClockEmulator):
        self._clock = clock

    def render(self, screen: pygame.Surface, pos: pygame.Rect) -> None:
        x = screen.get_size()[0] - 395
        y = screen.get_size()[1] - 200

        # background
        pygame.draw.rect(screen, (75, 75, 75), (x, y, x + 400, y + 200))

        fx = x + 45
        fy = y + 45

        # clocks
        clock_radius = 23
        dot_radius = 3

        for i, state in enumerate(self._clock.front.states + self._clock.back.states):
            state += 6
            state = -state
            state = state % 12

            x, y = i % 3 * 55 + fx, i // 3 * 55 + fy
            color = (77, 117, 255)
            if i >= 9:
                x += 195
                y -= 55 * 3
                color = (21, 96, 189)

            for j in range(12):
                pointer_color = tuple(min(color[i] + 30, 255) for i in range(3))
                game.draw_antialias_circle(screen, pointer_color,
                                           x + sin(j * (pi / 6)) * (clock_radius + dot_radius * 0),
                                           y + cos(j * (pi / 6)) * (clock_radius + dot_radius * 0),
                                           dot_radius)

            game.draw_antialias_circle(screen, color, x, y, clock_radius)

            game.draw_aa_pie(screen, (255, 255, 255), (x, y),
                             (x + sin(state * (pi / 6)) * clock_radius,
                              y + cos(state * (pi / 6)) * clock_radius), 3)

        # for i, state in enumerate(self.timer.clock.back.states):
        #     draw_antialias_circle(screen, (155, 177, 25), i % 3 * 55 + fx + 195, i // 3 * 55 + fy, 23)

        # pins
        front_pins = self._clock.pins
        back_pins = _invert_pins(front_pins)

        for i in range(front_pins.__len__()):

            color = (126, 126, 35)

            if front_pins[i]:
                color = (255, 255, 0)

            game.draw_antialias_circle(screen, color, i % 2 * 55 + fx + 28, i // 2 * 55 + fy + 28, 9)

        for i in range(back_pins.__len__()):

            color = (126, 126, 35)

            if back_pins[i]:
                color = (255, 255, 0)

            game.draw_antialias_circle(screen, color, i % 2 * 55 + fx + 28 + 194, i // 2 * 55 + fy + 28, 9)
