from enum import Enum
import re
from assets.puzzles.abstract_puzzle_emulator import AbstractPuzzleEmulator


class MoveMappings(Enum):

    UR = [0, 1, 1,
          0, 1, 1,
          0, 0, 0,

          -1, 0, 0,
          0, 0, 0,
          0, 0, 0
          ]

    DR = [0, 0, 0,
          0, 1, 1,
          0, 1, 1,

          0, 0, 0,
          0, 0, 0,
          -1, 0, 0
          ]

    DL = [0, 0, 0,
          1, 1, 0,
          1, 1, 0,

          0, 0, 0,
          0, 0, 0,
          0, 0, -1
          ]

    UL = [1, 1, 0,
          1, 1, 0,
          0, 0, 0,

          0, 0, -1,
          0, 0, 0,
          0, 0, 0
          ]

    U = [1, 1, 1,
         1, 1, 1,
         0, 0, 0,

         -1, 0, -1,
         0, 0, 0,
         0, 0, 0
         ]

    R = [0, 1, 1,
         0, 1, 1,
         0, 1, 1,

         -1, 0, 0,
         0, 0, 0,
         -1, 0, 0
         ]

    D = [0, 0, 0,
         1, 1, 1,
         1, 1, 1,

         0, 0, 0,
         0, 0, 0,
         -1, 0, -1
         ]

    L = [1, 1, 0,
         1, 1, 0,
         1, 1, 0,

         0, 0, -1,
         0, 0, 0,
         0, 0, -1
         ]

    ALL = [1, 1, 1,
           1, 1, 1,
           1, 1, 1,

           -1, 0, -1,
           0, 0, 0,
           -1, 0, -1
           ]

    BACKSLASH = [0, 1, 1,
                 1, 1, 1,
                 1, 1, 0,

                 -1, 0, 0,
                 0, 0, 0,
                 0, 0, -1
                 ]

    SLASH = [1, 1, 0,
             1, 1, 1,
             0, 1, 1,

             0, 0, -1,
             0, 0, 0,
             -1, 0, 0
             ]

    ur = [1, 1, 0,
          1, 1, 1,
          1, 1, 1,

          0, 0, -1,
          0, 0, 0,
          -1, 0, -1]

    dr = [1, 1, 1,
          1, 1, 1,
          1, 1, 0,

          -1, 0, -1,
          0, 0, 0,
          0, 0, -1]

    dl = [1, 1, 1,
          1, 1, 1,
          0, 1, 1,

          -1, 0, -1,
          0, 0, 0,
          -1, 0, 0]

    ul = [0, 1, 1,
          1, 1, 1,
          1, 1, 1,

          -1, 0, 0,
          0, 0, 0,
          -1, 0, -1]


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
                direction = int(items[2] + "1")  # indicates its direction that clock moves, +1 / -1

                if pin == "/":
                    pin = "SLASH"
                elif pin == "\\":
                    pin = "BACKSLASH"

                self.move_with(amount * direction, side, MoveMappings[pin].value)

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

        for i, rule in enumerate(method):
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
