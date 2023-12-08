import pygame.gfxdraw
import math
import copy
from assets.puzzles.abstract_puzzle_renderer import AbstractPuzzleRenderer
from assets.puzzles.pyraminx.emulator import PyraminxEmulator, Color, ColorSide, to_color_tuple


SCALE = 100
BORDER = 10
Tri = list[list[float]]

class PyraminxRenderer(AbstractPuzzleRenderer):
    def __init__(self, puzzle):
        self._puzzle: PyraminxEmulator = puzzle

    def render(self, screen: pygame.Surface, pos: pygame.Rect) -> None:
        x = screen.get_size()[0] - 300
        y = screen.get_size()[1] - 300

        # background
        pygame.draw.rect(screen, (75, 75, 75), (x, y, x + 400, y + 200))

        x += 25
        y += 60

        def fix_index_of_tris(tris) -> list: # AAAAAAAAAAAAAA @huu-bo why did you make this so difficult list swapping doesnt work

            res = copy.deepcopy(tris)

            res[1] = tris[2]
            res[2] = tris[3]
            res[3] = tris[1]
            res[5] = tris[7]
            res[7] = tris[5]
            res[6] = tris[8]
            res[8] = tris[6]

            res[8], res[7] = res[7], res[8]

            return res


        def mirror_tris(tris) -> list:

            res = copy.deepcopy(tris)

            res[1] = tris[3]
            res[3] = tris[1]
            res[4] = tris[8]
            res[5] = tris[7]
            res[7] = tris[5]
            res[8] = tris[4]

            return res


        def draw_side(sx, sy, flipped, side_color: Color):

            tris = piraminx_triangles(flipped)
            tris = fix_index_of_tris(tris)

            if side_color == Color.YELLOW:
                tris = mirror_tris(tris)

            for i, tri in enumerate(tris):

                side: ColorSide = self._puzzle.sides[side_color.value]

                piece_color = side.piece_side[i]

                pygame.gfxdraw.filled_polygon(screen,
                                              [(tri[i][0] * SCALE + x + sx, tri[i][1] * SCALE + y + sy) for i in
                                               range(3)], to_color_tuple(Color(piece_color)))

                pygame.draw.aalines(screen, (0, 0, 0), True,
                                    ([line for line in [(tri[i][0] * SCALE + x + sx, tri[i][1] * SCALE + y + sy) for i in range(3)]]), 0)

                # render text for debugging

                # tx = 0
                # ty = 0
                #
                # for p in [(tri[i][0] * SCALE + x + sx, tri[i][1] * SCALE + y + sy) for i in range(3)]:
                #     tx += p[0]
                #     ty += p[1]
                #
                # tx /= 3
                # ty /= 3
                #
                # screen.blit(pygame.font.Font("assets/fonts/font1.ttf", 15).render(f"{i}", True, (255, 255, 255)), (tx - 2, ty - 12))


        draw_side(0, SCALE - BORDER, False, Color.RED)
        draw_side(SCALE // 2 + BORDER, 100 - BORDER * 2, True, Color.YELLOW)
        draw_side(SCALE + BORDER * 2, SCALE - BORDER, False, Color.BLUE)
        draw_side(SCALE // 2 + BORDER, 0 - BORDER * 3, False, Color.GREEN)


def _get_line_middle_coords(line: list[list[float]]):

    top_to_right_angle = math.atan2(line[1][0] - line[0][0], line[1][1] - line[0][1])
    dist = math.sqrt((line[0][0] - line[1][0]) ** 2 + (line[0][1] - line[1][1]) ** 2)
    new_dist = dist / 2

    new_coord = [
        line[0][0] + math.sin(top_to_right_angle) * new_dist,
        line[0][1] + math.cos(top_to_right_angle) * new_dist
    ]

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

    tri = [[0.5, 0], [1, 1], [0, 1]]
    tris = _get_tri_sub(tri)
    out = []
    for t in tris:
        out += _get_tri_sub(t)

    rm = []
    for tri in out:
        for p in tri:
            if p[1] > .9:
                rm.append(tri)
    for tri in rm:
        if tri in out:
            out.remove(tri)

    highest = 0
    for tri in out:
        for p in tri:
            if p[1] > highest:
                highest = p[1]

    out = [[[p[0], p[1]] for p in tri] for tri in out]  # copy
    for tri in out:
        for p in tri:
            p[0] *= 1 / highest
            assert p[0] >= 0, p[0]
            assert p[1] <= highest
            p[1] *= 1 / highest

    if flipped:
        for tri in out:
            for i, coord in enumerate(tri):
                tri[i][1] = 1 - coord[1]

    # print("out:", out)

    return out


if __name__ == '__main__':
    print(_get_line_middle_coords([[0, 0], [1, 1]]))
    print(_get_line_middle_coords([[0, 0], [0, 1]]))
    print(_get_line_middle_coords([[0, 0], [1, 0]]))
