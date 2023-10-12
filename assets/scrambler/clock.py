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
        ]

        self.pins = [True, True,
                     True, True]

        self.front = Clock.Side(True)
        self.back = Clock.Side(False)



    def move(self, amount, pins: [int, int, int, int]):

        if pins[0] and pins[1] and pins[2] and pins[3]:
            self.move_with(amount, 8)
        elif pins[0] and not pins[1] and not pins[2] and not pins[3]:
            self.move_with(amount, 3)
        elif not pins[0] and pins[1] and not pins[2] and not pins[3]:
            self.move_with(amount, 0)
        elif not pins[0] and not pins[1] and pins[2] and not pins[3]:
            self.move_with(amount, 2)
        elif not pins[0] and not pins[1] and not pins[2] and pins[3]:
            self.move_with(amount, 1)
        elif pins[0] and pins[1] and not pins[2] and not pins[3]:
            self.move_with(amount, 4)
        elif pins[0] and pins[2] and not pins[1] and not pins[3]:
            self.move_with(amount, 7)
        elif pins[0] and pins[3] and not pins[1] and not pins[2]:
            self.move_with(amount, 10)
        elif pins[1] and pins[2] and not pins[3] and not pins[0]:
            self.move_with(amount, 9)
        elif pins[1] and pins[3] and not pins[0] and not pins[2]:
            self.move_with(amount, 5)
        elif pins[2] and pins[3] and not pins[0] and not pins[1]:
            self.move_with(amount, 6)
        else:
            print("not implemented")

    def move_with(self, amount, move_index):
        move_rule = self.MOVE_STATE[move_index]

        for i in range(move_rule.__len__()):

            rule = move_rule[i]

            if i < 9:
                if rule == 1:
                    self.front.states[i] += amount
                #elif rule == -1:
                    #self.front.states[i] -= amount
                    #print("how????")

            else:
                if rule == -1:
                    self.back.states[i - 9] -= amount
                else:
                    print("how????")

            #self.front.states[i] %= 12
            #self.back.states[i] %= 12


    class Side:

        def __init__(self, front):
            self.front = front
            self.states = [0, 0, 0,
                           0, 0, 0,
                           0, 0, 0]