from assets.puzzles.abstract_puzzle_emulator import AbstractPuzzleEmulator
from enum import Enum
import copy


class PyraminxEmulator(AbstractPuzzleEmulator):
    def __init__(self):
        self.sides = [
            ColorSide(Color.GREEN),
            ColorSide(Color.RED),
            ColorSide(Color.BLUE),
            ColorSide(Color.YELLOW)
        ]

        self.reset()

    def reset(self) -> None:
        for side in self.sides:
            side.reset()

    def convert_scramble(self, scramble: str) -> None:

        blocks = scramble.split(" ")

        for block in blocks:
            self.move(block)

    def move(self, notation: str) -> None:

        copy_sides = copy.deepcopy(self.sides)  # this took way to long to figure out...
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


PIECE_SIDES = 9

class Color(Enum):

    GREEN = 0
    RED = 1
    BLUE = 2
    YELLOW = 3


def to_color_tuple(color: Color):

    val = color

    if val == Color.GREEN:
        return 0, 255, 0
    elif val == Color.RED:
        return 255, 0, 0
    elif val == Color.BLUE:
        return 0, 0, 255
    elif val == Color.YELLOW:
        return 255, 255, 0
    else:
        raise ValueError("to_color_tuple() argument should be object 'GREEN', 'RED', 'BLUE' or 'YELLOW' inside class Color")

class ColorSide:

    def __init__(self, color: Color):
        self.color = color
        self.piece_side = []

    def reset(self):

        self.piece_side = []

        for i in range(PIECE_SIDES):
            self.piece_side.append(self.color.value)


def convert_normal_notation_to_mapping_enum_name(notation: str):  # I couldn't think of another name for this

    base = get_base_of_move(notation)

    if notation[0].islower():
        base = base.capitalize()
        base += "_TIP"

    if notation.count("'") > 0:
        base += "_PRIME"

    return base


def get_base_of_move(move: str):
    res = move
    res = res.replace(" ", "") # remove space
    res = res.replace("'", "") # remove prime

    return res