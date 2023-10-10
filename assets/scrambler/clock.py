import random


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


class Clock:

    def __init__(self):
        front = Clock.Side(True)
        back = Clock.Side(False)

    class Side:
        MOVE_STATE = [
            [0, 1, 1,
             0, 1, 1,
             0, 0, 0,

             -1, 0, 0,
             0, 0, 0,
             0, 0, 0
             ],  # UR

            [0, 0, 0,
             0, 1, 1,
             0, 1, 1,

             0, 0, 0,
             0, 0, 0,
             -1, 0, 0
             ],  # DR

            [0, 0, 0,
             1, 1, 0,
             1, 1, 0,

             0, 0, 0,
             0, 0, 0,
             0, 0, -1
             ],  # DL

            [1, 1, 0,
             1, 1, 0,
             0, 0, 0,

             0, 0, -1,
             0, 0, 0,
             0, 0, 0
             ],  # UL

            [1, 1, 1,
             1, 1, 1,
             0, 0, 0,

             -1, 0, -1,
             0, 0, 0,
             0, 0, 0
             ],  # U

            [0, 1, 1,
             0, 1, 1,
             0, 1, 1,

             -1, 0, 0,
             0, 0, 0,
             -1, 0, 0
             ],  # R

            [0, 0, 0,
             1, 1, 1,
             1, 1, 1,

             0, 0, 0,
             0, 0, 0,
             -1, 0, -1
             ],  # D

            [1, 1, 0,
             1, 1, 0,
             1, 1, 0,

             0, 0, -1,
             0, 0, 0,
             0, 0, -1
             ],  # L

            [1, 1, 1,
             1, 1, 1,
             1, 1, 1,

             -1, 0, -1,
             0, 0, 0,
             -1, 0, -1
             ],  # ALL

            [0, 1, 1,
             1, 1, 1,
             1, 1, 0,

             -1, 0, 0,
             0, 0, 0,
             0, 0, -1
             ],  # /

            [1, 1, 0,
             1, 1, 1,
             0, 1, 1,

             0, 0, -1,
             0, 0, 0,
             -1, 0, 0
             ],  # \
        ]

        def __init__(self, front):
            self.front = front
            self.pins = [1, 1,
                         1, 1]
            self.states = [0, 0, 0,
                           0, 0, 0,
                           0, 0, 0]
