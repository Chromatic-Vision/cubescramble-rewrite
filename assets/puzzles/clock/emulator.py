import re
from assets.puzzles.abstract_puzzle_emulator import AbstractPuzzleEmulator

_MOVE_MAPPINGS = [
    [0, 1, 1,
     0, 1, 1,
     0, 0, 0,

     -1, 0, 0,
     0, 0, 0,
     0, 0, 0
     ],  # UR, 0

    [0, 0, 0,
     0, 1, 1,
     0, 1, 1,

     0, 0, 0,
     0, 0, 0,
     -1, 0, 0
     ],  # DR, 1

    [0, 0, 0,
     1, 1, 0,
     1, 1, 0,

     0, 0, 0,
     0, 0, 0,
     0, 0, -1
     ],  # DL, 2

    [1, 1, 0,
     1, 1, 0,
     0, 0, 0,

     0, 0, -1,
     0, 0, 0,
     0, 0, 0
     ],  # UL, 3

    [1, 1, 1,
     1, 1, 1,
     0, 0, 0,

     -1, 0, -1,
     0, 0, 0,
     0, 0, 0
     ],  # U, 4

    [0, 1, 1,
     0, 1, 1,
     0, 1, 1,

     -1, 0, 0,
     0, 0, 0,
     -1, 0, 0
     ],  # R, 5

    [0, 0, 0,
     1, 1, 1,
     1, 1, 1,

     0, 0, 0,
     0, 0, 0,
     -1, 0, -1
     ],  # D, 6

    [1, 1, 0,
     1, 1, 0,
     1, 1, 0,

     0, 0, -1,
     0, 0, 0,
     0, 0, -1
     ],  # L, 7

    [1, 1, 1,
     1, 1, 1,
     1, 1, 1,

     -1, 0, -1,
     0, 0, 0,
     -1, 0, -1
     ],  # ALL, 8

    [0, 1, 1,
     1, 1, 1,
     1, 1, 0,

     -1, 0, 0,
     0, 0, 0,
     0, 0, -1
     ],  # /, 9

    [1, 1, 0,
     1, 1, 1,
     0, 1, 1,

     0, 0, -1,
     0, 0, 0,
     -1, 0, 0
     ],  # \, 10

    [1, 1, 0,
     1, 1, 1,
     1, 1, 1,

     0, 0, -1,
     0, 0, 0,
     -1, 0, -1],  # ur, 11

    [1, 1, 1,
     1, 1, 1,
     1, 1, 0,

     -1, 0, -1,
     0, 0, 0,
     0, 0, -1],  # dr, 12

    [1, 1, 1,
     1, 1, 1,
     0, 1, 1,

     -1, 0, -1,
     0, 0, 0,
     -1, 0, 0],  # dl, 13

    [0, 1, 1,
     1, 1, 1,
     1, 1, 1,

     -1, 0, 0,
     0, 0, 0,
     -1, 0, -1],  # ul, 14
]


class ClockEmulator(AbstractPuzzleEmulator):
    def __init__(self):
        self.pins = [True, True,
                     True, True]

        self.front = ClockEmulator.Side(True)
        self.back = ClockEmulator.Side(False)

    def reset(self) -> None:
        self.front.states = [0, 0, 0,
                             0, 0, 0,
                             0, 0, 0]
        self.back.states = [0, 0, 0,
                            0, 0, 0,
                            0, 0, 0]

        self.pins = [True, True,
                     True, True]

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
                direction = int(items[2] + "1")  # indicates its direction that clock moves, e.g. +

                if pin == "UR":
                    self.move_with(amount * direction, side, 0)
                elif pin == "DR":
                    self.move_with(amount * direction, side, 1)
                elif pin == "DL":
                    self.move_with(amount * direction, side, 2)
                elif pin == "UL":
                    self.move_with(amount * direction, side, 3)
                elif pin == "U":
                    self.move_with(amount * direction, side, 4)
                elif pin == "R":
                    self.move_with(amount * direction, side, 5)
                elif pin == "D":
                    self.move_with(amount * direction, side, 6)
                elif pin == "L":
                    self.move_with(amount * direction, side, 7)
                elif pin == "ALL":
                    self.move_with(amount * direction, side, 8)
            else:  # special cases
                pin = str(block)

                if pin == "y2":
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
        move_rule = _MOVE_MAPPINGS[method]

        for i, rule in enumerate(move_rule):
            if i < 9:
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

            else:
                if side == 0:
                    if rule == -1:
                        self.back.states[i - 9] -= amount
                    elif rule == 1:
                        assert False
                elif side == 1:
                    if rule == -1:
                        self.front.states[i - 9] -= amount
                    elif rule == 1:
                        assert False

                self.back.states[i - 9] %= 12
                self.front.states[i - 9] %= 12

    class Side:
        def __init__(self, front: bool):
            self.front: bool = front
            self.states = [0, 0, 0,
                           0, 0, 0,
                           0, 0, 0]
