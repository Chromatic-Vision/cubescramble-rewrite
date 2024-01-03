import copy
from enum import Enum
import re
from assets.puzzles.abstract_puzzle_emulator import AbstractPuzzleEmulator


class MoveMappings(Enum):

    UR = [[0, 1, 1,
          0, 1, 1,
          0, 0, 0],

          [-1, 0, 0,
          0, 0, 0,
          0, 0, 0]
          ]

    DR = [[0, 0, 0,
          0, 1, 1,
          0, 1, 1],

          [0, 0, 0,
          0, 0, 0,
          -1, 0, 0]
          ]

    DL = [[0, 0, 0,
          1, 1, 0,
          1, 1, 0],

          [0, 0, 0,
          0, 0, 0,
          0, 0, -1]
          ]

    UL = [[1, 1, 0,
          1, 1, 0,
          0, 0, 0],

          [0, 0, -1,
          0, 0, 0,
          0, 0, 0]
          ]

    U = [[1, 1, 1,
         1, 1, 1,
         0, 0, 0],

         [-1, 0, -1,
         0, 0, 0,
         0, 0, 0]
         ]

    R = [[0, 1, 1,
         0, 1, 1,
         0, 1, 1],

         [-1, 0, 0,
         0, 0, 0,
         -1, 0, 0]
         ]

    D = [[0, 0, 0,
         1, 1, 1,
         1, 1, 1],

         [0, 0, 0,
         0, 0, 0,
         -1, 0, -1]
         ]

    L = [[1, 1, 0,
         1, 1, 0,
         1, 1, 0],

         [0, 0, -1,
         0, 0, 0,
         0, 0, -1]
         ]

    ALL = [[1, 1, 1,
           1, 1, 1,
           1, 1, 1],

           [-1, 0, -1,
           0, 0, 0,
           -1, 0, -1]
           ]

    BACKSLASH = [[0, 1, 1,
                 1, 1, 1,
                 1, 1, 0],

                 [-1, 0, 0,
                 0, 0, 0,
                 0, 0, -1]
                 ]

    SLASH = [[1, 1, 0,
             1, 1, 1,
             0, 1, 1],

             [0, 0, -1,
             0, 0, 0,
             -1, 0, 0]
             ]

    ur = [[1, 1, 0,
          1, 1, 1,
          1, 1, 1],

          [0, 0, -1,
          0, 0, 0,
          -1, 0, -1]]

    dr = [[1, 1, 1,
          1, 1, 1,
          1, 1, 0],

          [-1, 0, -1,
          0, 0, 0,
          0, 0, -1]]

    dl = [[1, 1, 1,
          1, 1, 1,
          0, 1, 1],

          [-1, 0, -1,
          0, 0, 0,
          -1, 0, 0]]

    ul = [[0, 1, 1,
          1, 1, 1,
          1, 1, 1],

          [-1, 0, 0,
          0, 0, 0,
          -1, 0, -1]]


class ClockEmulator(AbstractPuzzleEmulator):
    def __init__(self):
        self.pins = [True, True,
                     True, True]

        self.front = ClockEmulator.Side(True)
        self.back = ClockEmulator.Side(False)

        self.rotation = 0 # 0 = 0d, 1 = 45d, 2 = 90d, 3 = 135d (clockwise) (works glitchy) # TODO: fix this
        # self.focus = 0 # 0 = front, 1 = back

    def reset(self) -> None:
        self.front.states = [0, 0, 0,
                             0, 0, 0,
                             0, 0, 0]
        self.back.states = [0, 0, 0,
                            0, 0, 0,
                            0, 0, 0]

        self.pins = [True, True,
                     True, True]

        self.rotation = 0

    def move(self, s: str) -> None:  # bruh, at least it sort of like works
        self.convert_scramble(s)

    def convert_scramble(self, scramble: str) -> None:
        blocks = scramble.split(" ")

        side = 0  # side where we're working at, 0 is front, 1 is back

        for block in blocks:
            match = re.match(r'([A-Z]+)(\d+)([+-])', str(block), re.I)  # split scramble block

            if match:
                items = match.groups()

                pin = items[0]  # pin, e.g. UR
                amount = int(items[1])  # amount, e.g. 5
                direction = int(items[2] + "1")  # indicates its direction that clock moves, +1 / -1

                if pin == "/":
                    pin = "SLASH"
                elif pin == "\\":
                    pin = "BACKSLASH"

                self.move_with(amount * direction, side, MoveMappings[pin].value)

            else:  # special cases

                pin = str(block)

                if pin == "z":

                    if side == 0:
                        self.rotation += 1
                    elif side == 1:
                        self.rotation -= 1

                    self.rotation %= 4

                elif pin == "z'":

                    if side == 0:
                        self.rotation -= 1
                    elif side == 1:
                        self.rotation += 1

                    self.rotation %= 4

                elif pin == "z2":

                    self.rotation += 2
                    self.rotation %= 4

                elif pin == "x2":

                    self.rotation += 2
                    self.rotation %= 4
                    side = 0 if side == 1 else 1

                elif pin == "y2": # TODO: y2 mid solve causes pins to go down ??

                    if side == 0:
                        self.pins = [True, True,
                                     True, True]
                        side = 1

                    elif side == 1:
                        self.pins = [False, False,
                                     False, False]
                        side = 0

                if side == 0:
                    if pin == "UR":
                        self.pins[1] = True
                    elif pin == "DR":
                        self.pins[3] = True
                    elif pin == "DL":
                        self.pins[2] = True
                    elif pin == "UL":
                        self.pins[0] = True
                elif side == 1:
                    if pin == "UR":
                        self.pins[0] = False
                    elif pin == "DR":
                        self.pins[2] = False
                    elif pin == "DL":
                        self.pins[3] = False
                    elif pin == "UL":
                        self.pins[1] = False

    def move_with(self, amount, side, method):  # this code sucks ngl

        relative_front = method[0]
        relative_back = method[1]

        for _ in range(self.rotation):
            relative_front = self.rotate_matrix(relative_front, True)
            relative_back = self.rotate_matrix(relative_back, False)

        for i, rule in enumerate(relative_front):
            if side == 0:
                if rule == 1:
                    self.front.states[i] += amount
                elif rule == -1:
                    assert False
            elif side == 1:
                if rule == 1:
                    self.back.states[i] += amount
                elif rule == -1:
                    assert False

            self.front.states[i] %= 12
            self.back.states[i] %= 12

        for i, rule in enumerate(relative_back):

            if side == 0:
                if rule == -1:
                    self.back.states[i] -= amount
                elif rule == 1:
                    assert False
            elif side == 1:
                if rule == -1:
                    self.front.states[i] -= amount
                elif rule == 1:
                    assert False

            self.back.states[i] %= 12
            self.front.states[i] %= 12

    class Side:
        def __init__(self, front: bool):
            self.front: bool = front
            self.states = [0, 0, 0,
                           0, 0, 0,
                           0, 0, 0]

    def get_piece(self, side: int, piece: int) -> int:

        if side == 0:

            k = self.front.states

            for _ in range(self.rotation):
                k = self.rotate_matrix(k, True)

        elif side == 1:

            k = self.back.states

            for _ in range(self.rotation):
                k = self.rotate_matrix(k, False)

        else:

            raise ValueError("Side must be 0 or 1")

        return k[piece]


    def rotate_matrix(self, matrix, clockwise: bool):

        if matrix.__len__() != 9:
            raise ValueError(f"Length {matrix.__len__()} is not supported, the length should be 9")

        if clockwise:

            w = copy.deepcopy(matrix)
            res = [w[6], w[3], w[0], w[7], w[4], w[1], w[8], w[5], w[2]]

            return res

        else:

            w = copy.deepcopy(matrix)
            res = [w[2], w[5], w[8], w[1], w[4], w[7], w[0], w[3], w[6]]

            return res




    def get_clock_piece_from_notation(self, side: int, notation: str, rotation: str) -> int: # lowercase is "white": the side you start memorizing from. uppercase is "black": the side where you start from.

            if side == 0: # front

                if rotation == "x2":
                    return {

                        'ul': self.get_piece(1, 0),
                        'u': self.get_piece(1, 1),
                        'ur': self.get_piece(1, 2),
                        'l': self.get_piece(1, 3),
                        'c': self.get_piece(1, 4),
                        'r': self.get_piece(1, 5),
                        'dl': self.get_piece(1, 6),
                        'd': self.get_piece(1, 7),
                        'dr': self.get_piece(1, 8),
                        'UL': self.get_piece(0, 8),
                        'U': self.get_piece(0, 7),
                        'UR': self.get_piece(0, 6),
                        'L': self.get_piece(0, 5),
                        'C': self.get_piece(0, 4),
                        'R': self.get_piece(0, 3),
                        'DL': self.get_piece(0, 2),
                        'D': self.get_piece(0, 1),
                        'DR': self.get_piece(0, 0)

                    }.get(notation, 11)

                elif rotation == "y2":
                    return {

                        'ul': self.get_piece(1, 0),
                        'u': self.get_piece(1, 1),
                        'ur': self.get_piece(1, 2),
                        'l': self.get_piece(1, 3),
                        'c': self.get_piece(1, 4),
                        'r': self.get_piece(1, 5),
                        'dl': self.get_piece(1, 6),
                        'd': self.get_piece(1, 7),
                        'dr': self.get_piece(1, 8),
                        'UL': self.get_piece(0, 0),
                        'U': self.get_piece(0, 1),
                        'UR': self.get_piece(0, 2),
                        'L': self.get_piece(0, 3),
                        'C': self.get_piece(0, 4),
                        'R': self.get_piece(0, 5),
                        'DL': self.get_piece(0, 6),
                        'D': self.get_piece(0, 7),
                        'DR': self.get_piece(0, 8)

                    }.get(notation, 11)

            elif side == 1:

                if rotation == "x2":
                    return {

                        'ul': self.get_piece(0, 0),
                        'u': self.get_piece(0, 1),
                        'ur': self.get_piece(0, 2),
                        'l': self.get_piece(0, 3),
                        'c': self.get_piece(0, 4),
                        'r': self.get_piece(0, 5),
                        'dl': self.get_piece(0, 6),
                        'd': self.get_piece(0, 7),
                        'dr': self.get_piece(0, 8),
                        'UL': self.get_piece(1, 8),
                        'U': self.get_piece(1, 7),
                        'UR': self.get_piece(1, 6),
                        'L': self.get_piece(1, 5),
                        'C': self.get_piece(1, 4),
                        'R': self.get_piece(1, 3),
                        'DL': self.get_piece(1, 2),
                        'D': self.get_piece(1, 1),
                        'DR': self.get_piece(1, 0)

                    }.get(notation, 11)

                elif rotation == "y2":
                    return {

                        'ul': self.get_piece(0, 0),
                        'u': self.get_piece(0, 1),
                        'ur': self.get_piece(0, 2),
                        'l': self.get_piece(0, 3),
                        'c': self.get_piece(0, 4),
                        'r': self.get_piece(0, 5),
                        'dl': self.get_piece(0, 6),
                        'd': self.get_piece(0, 7),
                        'dr': self.get_piece(0, 8),
                        'UL': self.get_piece(1, 0),
                        'U': self.get_piece(1, 1),
                        'UR': self.get_piece(1, 2),
                        'L': self.get_piece(1, 3),
                        'C': self.get_piece(1, 4),
                        'R': self.get_piece(1, 5),
                        'DL': self.get_piece(1, 6),
                        'D': self.get_piece(1, 7),
                        'DR': self.get_piece(1, 8)

                    }.get(notation, 11)
