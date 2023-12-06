import pygame
import math
from assets.puzzles.abstract_puzzle_renderer import AbstractPuzzleRenderer
from assets.puzzles.pyraminx.emulator import PyraminxEmulator


SCALE = 100
Tri = list[list[float]]
# TODO: renderer is not done yet


class PyraminxRenderer(AbstractPuzzleRenderer):
    def __init__(self, puzzle):
        self._puzzle: PyraminxEmulator = puzzle

    def render(self, screen: pygame.Surface, pos: pygame.Rect) -> None:
        x = screen.get_size()[0] - 395
        y = screen.get_size()[1] - 200

        # background
        pygame.draw.rect(screen, (75, 75, 75), (x, y, x + 400, y + 200))

        tris = piraminx_triangles(False)
        for tri in tris:
            pygame.draw.polygon(screen, (255, 255, 255),
                                [(tri[i][0] * SCALE + x, tri[i][1] * SCALE + y) for i in range(3)], 2)


def _get_line_middle_coords(line: list[list[float]]):
    # top, right, left
    # top_to_right_angle = math.atan2(line[0][0] - line[1][0], line[0][1] - line[1][1])
    top_to_right_angle = math.atan2(line[1][0] - line[0][0], line[1][1] - line[0][1])
    # print(top_to_right_angle)
    dist = math.sqrt((line[0][0] - line[1][0]) ** 2 + (line[0][1] - line[1][1]) ** 2)
    new_dist = dist / 2
    # print(dist, new_dist)

    new_coord = [
        line[0][0] + math.sin(top_to_right_angle) * new_dist,
        line[0][1] + math.cos(top_to_right_angle) * new_dist
    ]
    # print(new_coord)
    return new_coord


def _get_tri_sub(tri: Tri) -> list[Tri]:
    middles = [_get_line_middle_coords(line) for line in [[tri[i % 3], tri[(i + 1) % 3]] for i in range(3)]]

    # A31
    # C32
    # B12
    # 123
    return [
        [
            tri[0],
            middles[2],
            middles[0]
        ],
        [
            tri[2],
            middles[2],
            middles[1]
        ],
        [
            tri[1],
            middles[0],
            middles[1]
        ],
        [
            middles[0],
            middles[1],
            middles[2]
        ]
    ]


def piraminx_triangles(flipped: bool) -> list[Tri]:
    tri = [[0, 0], [1, 1], [-1, 1]]
    tris = _get_tri_sub(tri)
    out = []
    for t in tris:
        out += _get_tri_sub(t)

    if flipped:
        for tri in out:
            for i, coord in enumerate(tri):
                tri[i][1] = 1 - coord[1]

    return out


if __name__ == '__main__':
    print(_get_line_middle_coords([[0, 0], [1, 1]]))
    print(_get_line_middle_coords([[0, 0], [0, 1]]))
    print(_get_line_middle_coords([[0, 0], [1, 0]]))

    # assert _get_line_middle_coords([[0, 0], [1, 1]]) == [0.5, 0.5]
    # assert _get_line_middle_coords([[0, 0], [0, 1]]) == [0, 0.5]
    # assert _get_line_middle_coords([[0, 0], [1, 0]]) == [0.5, 0]
