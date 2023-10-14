import random
import re

# TODO: simultaneously moves


def get_scramble():
    scramble = ""

    scramble += "UR" + random_rotation() + " "
    scramble += "DR" + random_rotation() + " "
    scramble += "DL" + random_rotation() + " "
    scramble += "UL" + random_rotation() + " "
    scramble += "U" + random_rotation() + " "
    scramble += "R" + random_rotation() + " "
    scramble += "D" + random_rotation() + " "
    scramble += "L" + random_rotation() + " "
    scramble += "ALL" + random_rotation() + " "
    scramble += "y2"
    scramble += " "
    scramble += "U" + random_rotation() + " "
    scramble += "R" + random_rotation() + " "
    scramble += "D" + random_rotation() + " "
    scramble += "L" + random_rotation()
    scramble += random_pins()

    return scramble


def random_rotation():
    res = ""
    number = random.randint(0, 6)

    res += str(number)

    if 0 < number < 6:
        if bool(random.getrandbits(1)):
            res += "+"
        else:
            res += "-"
    else:
        res += "+"

    return res


def random_pins():
    res = ""

    for i in range(4):
        if bool(random.getrandbits(1)):
            if i == 0:
                res += " UR"
            if i == 1:
                res += " DR"
            if i == 2:
                res += " DL"
            if i == 3:
                res += " UL"

    return res


def invert_pins(pins):
    return [not pins[1], not pins[0], not pins[3], not pins[2]]

class Clock:

    def __init__(self):

        self.MOVE_STATE = [
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

        self.pins = [True, True,
                     True, True]

        self.front = Clock.Side(True)
        self.back = Clock.Side(False)

    def reset(self):
        self.front.states = [0, 0, 0,
                             0, 0, 0,
                             0, 0, 0]

        self.back.states = [0, 0, 0,
                            0, 0, 0,
                            0, 0, 0]
        self.pins = [True, True,
                     True, True]

    def convert_scramble(self, scramble: str):

        blocks = scramble.split(" ")
        
        side = 0 # side where we're working at, 0 is front, 1 is back

        for block in blocks:

            match = re.match(r'([A-Z]+)(\d+)([+-])', str(block), re.I) # split scramble block

            if match:
                
                items = match.groups()

                pin = items[0] # pin, e.g. UR
                amount = int(items[1]) # amount, e.g. 5
                direction = int(items[2] + "1") # indicates its direction that clock moves, e.g. +

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
            else: # special cases

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

    def move(self, amount, side, pins: [int, int, int, int]): # bruh, at least it sort of like works

        if not pins[0] and pins[1] and not pins[2] and not pins[3]:
            self.move_with(amount, side, 0) # UR
        elif not pins[0] and not pins[1] and not pins[2] and pins[3]:
            self.move_with(amount, side, 1) # DR
        elif not pins[0] and not pins[1] and pins[2] and not pins[3]:
            self.move_with(amount, side, 2) # DL
        elif pins[0] and not pins[1] and not pins[2] and not pins[3]:
            self.move_with(amount, side, 3) # UL
        elif pins[0] and pins[1] and not pins[2] and not pins[3]:
            self.move_with(amount, side, 4) # U
        elif not pins[0] and pins[1] and pins[3] and not pins[2]:
            self.move_with(amount, side, 5) # R
        elif not pins[0] and not pins[1] and pins[2] and pins[3]:
            self.move_with(amount, side, 6) # D
        elif pins[0] and not pins[1] and pins[2] and not pins[3]:
            self.move_with(amount, side, 7) # L
        elif pins[0] and pins[1] and pins[2] and pins[3]:
            self.move_with(amount, side, 8) # ALL
        elif not pins[0] and pins[1] and pins[2] and not pins[3]:
            self.move_with(amount, side, 9) # /
        elif pins[0] and not pins[1] and not pins[2] and pins[3]:
            self.move_with(amount, side, 10) # \
        elif pins[0] and not pins[1] and pins[2] and pins[3]:
            self.move_with(amount, side, 11) # ul
        elif pins[0] and pins[1] and pins[2] and not pins[3]:
            self.move_with(amount, side, 12) # dr
        elif pins[0] and pins[1] and not pins[2] and pins[3]:
            self.move_with(amount, side, 13) # dl
        elif not pins[0] and pins[1] and pins[2] and pins[3]:
            self.move_with(amount, side, 14) # ul
        else:
            print(f"Unimplemented move! Pins: {str(self.pins)}")

    def move_with(self, amount, side, method): # this code sucks ngl

        move_rule = self.MOVE_STATE[method]

        for i in range(move_rule.__len__()):

            rule = move_rule[i]

            if i < 9:

                if side == 0:
                    if rule == 1:
                        self.front.states[i] += amount
                    elif rule == -1:
                        print(
                            f"Unexpected move state -1 at index {i} found. You can ignore this error if you are modding this software.")
                elif side == 1:
                    if rule == 1:
                        self.back.states[i] += amount
                    elif rule == -1:
                        print(
                            f"Unexpected move state -1 at index {i} found. You can ignore this error if you are modding this software.")

                self.front.states[i] %= 12
                self.back.states[i] %= 12

            else:

                if side == 0:
                    if rule == -1:
                        self.back.states[i - 9] -= amount
                    elif rule == 1:
                        print(
                            f"Unexpected move state 1 at index {i} found. You can ignore this error if you are modding this software.")
                elif side == 1:
                    if rule == -1:
                        self.front.states[i - 9] -= amount
                    elif rule == 1:
                        print(
                            f"Unexpected move state 1 at index {i} found. You can ignore this error if you are modding this software.")


                self.back.states[i - 9] %= 12
                self.front.states[i - 9] %= 12


    class Side:

        def __init__(self, front):
            self.front = front
            self.states = [0, 0, 0,
                           0, 0, 0,
                           0, 0, 0]