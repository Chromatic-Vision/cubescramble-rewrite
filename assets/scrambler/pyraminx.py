import random
import copy
import math

from enum import Enum

moves = ["L", "R", "B", "U"]

def get_scramble():

    rm = []

    for i in range(8):

        move = random_move()

        if len(rm) > 0: # if the scramble is not empty, check if the next base move equals to the previous one

            while get_base_of_move(move) == get_base_of_move(rm[i - 1]):
                move = random_move()

        rm.append(move)

    scramble = " ".join(rm) + random_tips()

    return scramble

def get_base_of_move(move: str):
    res = move
    res = res.replace(" ", "") # remove space
    res = res.replace("'", "") # remove prime

    return res

def random_move():
    return random.choice(moves) + prime_random()

def random_tips():
    res = ""

    for i in range(4):
        if bool(random.getrandbits(1)):
            if i == 0:
                res += " l"
                res += prime_random()

            if i == 1:
                res += " r"
                res += prime_random()

            if i == 2:
                res += " b"
                res += prime_random()

            if i == 3:
                res += " u"
                res += prime_random()

    return res

def prime_random():
    if bool(random.getrandbits(1)):
        return "'"
    else:
        return ""


class Color:

    GREEN = 0
    RED = 1
    BLUE = 2
    YELLOW = 3

PIECE_SIDES = 9

class MoveMappings(Enum):

    L = [ # index 0 = GREEN, 1 = RED, BLUE = 2, YELLOW = 3, (COLOR_FROM, ORIGIN_INDEX)
        [
            None,
            (1, 6), None, None,
            (1, 8), (1, 7), (1, 3), None, None
        ],
        [
            None,
            None, None, (3, 3),
            None, None, (3, 6), (3, 7), (3, 8)
        ],
        [
            None,
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            None, None, (0, 6),
            None, None, (0, 1), (0, 5), (0, 4) # Yellow is a little bit weird because we flip the shape here...
        ]
    ]

    L_PRIME = [
        [
            None,
            (3, 6), None, None,
            (3, 8), (3, 7), (3, 3), None, None
        ],
        [
            None,
            None, None, (0, 6),
            None, None, (0, 1), (0, 5), (0, 4)
        ],
        [
            None,
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            None, None, (1, 3),
            None, None, (1, 6), (1, 7), (1, 8)
        ]
    ]

    R = [
        [
            None,
            None, None, (3, 6),
            None, None, (3, 1), (3, 5), (3, 4)
        ],
        [
            None,
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            (0, 6), None, None,
            (0, 8), (0, 7), (0, 3), None, None
        ],
        [
            None,
            (2, 1), None, None,
            (2, 4), (2, 5), (2, 6), None, None
        ]
    ]

    R_PRIME = [
        [
            None,
            None, None, (2, 6),
            None, None, (2, 1), (2, 5), (2, 4)
        ],
        [
            None,
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            (3, 1), None, None,
            (3, 4), (3, 5), (3, 6), None, None
        ],
        [
            None,
            (0, 6), None, None,
            (0, 8), (0, 7), (0, 3), None, None
        ]
    ]

    B = [
        [
            None,
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            (2, 6), None, None,
            (2, 8), (2, 7), (2, 3), None, None
        ],
        [
            None,
            None, None, (3, 1),
            None, None, (3, 3), (3, 2), (3, 0)
        ],
        [
            (1, 4),
            (1, 6), (1, 5), (1, 1),
            None, None, None, None, None
        ]
    ]

    B_PRIME = [
        [
            None,
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            (3, 3), None, None,
            (3, 0), (3, 2), (3, 1), None, None
        ],
        [
            None,
            None, None, (1, 6),
            None, None, (1, 1), (1, 5), (1, 4)
        ],
        [
            (2, 8),
            (2, 3), (2, 7), (2, 6),
            None, None, None, None, None
        ]
    ]

    U = [
        [
            (2, 0),
            (2, 1), (2, 2), (2, 3),
            None, None, None, None, None
        ],
        [
            (0, 0),
            (0, 1), (0, 2), (0, 3),
            None, None, None, None, None
        ],
        [
            (1, 0),
            (1, 1), (1, 2), (1, 3),
            None, None, None, None, None
        ],
        [
            None,
            None, None, None,
            None, None, None, None, None
        ]
    ]

    U_PRIME = [
        [
            (1, 0),
            (1, 1), (1, 2), (1, 3),
            None, None, None, None, None
        ],
        [
            (2, 0),
            (2, 1), (2, 2), (2, 3),
            None, None, None, None, None
        ],
        [
            (0, 0),
            (0, 1), (0, 2), (0, 3),
            None, None, None, None, None
        ],
        [
            None,
            None, None, None,
            None, None, None, None, None
        ]
    ]

    L_TIP = [
        [
            None,
            None, None, None,
            (1, 8), None, None, None, None
        ],
        [
            None,
            None, None, None,
            None, None, None, None, (3, 8)
        ],
        [
            None,
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            None, None, None,
            None, None, None, None, (0, 4)
        ]
    ]

    L_TIP_PRIME = [
        [
            None,
            None, None, None,
            (3, 8), None, None, None, None
        ],
        [
            None,
            None, None, None,
            None, None, None, None, (0, 4)
        ],
        [
            None,
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            None, None, None,
            None, None, None, None, (1, 8)
        ]
    ]

    R_TIP = [
        [
            None,
            None, None, None,
            None, None, None, None, (3, 4)
        ],
        [
            None,
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            None, None, None,
            (0, 8), None, None, None, None
        ],
        [
            None,
            None, None, None,
            (2, 4), None, None, None, None
        ]
    ]

    R_TIP_PRIME = [
        [
            None,
            None, None, None,
            None, None, None, None, (2, 4)
        ],
        [
            None,
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            None, None, None,
            (3, 4), None, None, None, None
        ],
        [
            None,
            None, None, None,
            (0, 8), None, None, None, None
        ]
    ]

    B_TIP = [
        [
            None,
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            None, None, None,
            (2, 8), None, None, None, None
        ],
        [
            None,
            None, None, None,
            None, None, None, None, (3, 0)
        ],
        [
            (1, 3),
            None, None, None,
            None, None, None, None, None
        ]
    ]

    B_TIP_PRIME = [
        [
            None,
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            None, None, None,
            (3, 0), None, None, None, None
        ],
        [
            None,
            None, None, None,
            None, None, None, None, (1, 4)
        ],
        [
            (2, 8),
            None, None, None,
            None, None, None, None, None
        ]
    ]

    U_TIP = [
        [
            (2, 0),
            None, None, None,
            None, None, None, None, None
        ],
        [
            (0, 0),
            None, None, None,
            None, None, None, None, None
        ],
        [
            (1, 0),
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            None, None, None,
            None, None, None, None, None
        ]
    ]

    U_TIP_PRIME = [
        [
            (1, 0),
            None, None, None,
            None, None, None, None, None
        ],
        [
            (2, 0),
            None, None, None,
            None, None, None, None, None
        ],
        [
            (0, 0),
            None, None, None,
            None, None, None, None, None
        ],
        [
            None,
            None, None, None,
            None, None, None, None, None
        ]
    ]


class ColorSide:

    def __init__(self, color: int):
        self.color = color
        self.piece_side = []

    def reset(self):

        self.piece_side = []

        for i in range(PIECE_SIDES):
            self.piece_side.append(self.color)

def convert_normal_notation_to_mapping_enum_name(notation: str): # I couldn't think of another name for this

    base = get_base_of_move(notation)

    if notation[0].islower():
        base = base.capitalize()
        base += "_TIP"

    if notation.count("'") > 0:
        base += "_PRIME"

    return base

class Pyraminx:

    def __init__(self):
        self.sides = [
            ColorSide(Color.GREEN),
            ColorSide(Color.RED),
            ColorSide(Color.BLUE),
            ColorSide(Color.YELLOW)
        ]

        self.reset_puzzle()

    def reset_puzzle(self):
        for side in self.sides:
            side.reset()

    def convert_scramble(self, scramble: str):

        blocks = scramble.split(" ")

        for block in blocks:
            self.move(block)


    def move(self, notation: str):

        copy_sides = copy.deepcopy(self.sides) # this took way to long to figure out...
        move_mapping = MoveMappings.__getitem__(convert_normal_notation_to_mapping_enum_name(notation)).value

        for i in range(len(self.sides)):

            instructions = move_mapping[i]

            side = self.sides[i]

            for j in range(len(side.piece_side)):

                if instructions[j] is None:
                    continue

                origin_color = instructions[j][0]
                origin_piece = instructions[j][1]

                origin_side = copy_sides[origin_color]

                side.piece_side[j] = origin_side.piece_side[origin_piece]


def _get_line_middle_coords(line: list[list[int]]):
    # top, right, left
    top_to_right_angle = math.atan2(line[0][0] - line[1][0], line[0][1] - line[1][1])
    print(top_to_right_angle)
    dist = math.sqrt((line[0][0] - line[1][0]) ** 2 + (line[0][1] - line[1][1]) ** 2)
    new_dist = dist / 2
    print(dist, new_dist)

    new_coord = [
        line[0][0] + math.sin(dist) * new_dist,
        line[0][1] + math.cos(dist) * new_dist
    ]
    print(new_coord)
    return new_coord

def _get_tri_sub(tri: list[list[int]]) -> list[list[list[float]]]:
    middles = [_get_line_middle_coords(line) for line in [[tri[i % 3], tri[(i + 1) % 3]] for i in range(3)]]

    # A31
    # C32
    # B12
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
        ]
    ]

def piraminx_triangles(flipped: bool) -> list[list[list[int]]]:
    tri = [[0, 0], [1, 1], [-1, 1]]
    tri = _get_line_middle_coords(tri)
    tri = _get_line_middle_coords(tri)


if __name__ == "__main__":

    pm = Pyraminx()

    a = get_scramble()
    print(a)

    pm.convert_scramble(a)

    for nb in pm.sides:
        print(nb.piece_side)

    print(_get_line_middle_coords([[0, 0], [1, 1], [-1, 1]]))
    print(_get_tri_sub([[0, 0], [1, 1], [-1, 1]]))
