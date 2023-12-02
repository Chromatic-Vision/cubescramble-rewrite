import random
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

    L = [ # index 0 = GREEN, 1 = RED, BLUE = 2, YELLOW = 3
        [
            -1,
            1, -1, -1,
            1, 1, 1, -1, -1 # Here it indicates that 4 pieces on the left side from red side will move to the green side. -1 means it won't move.
        ],
        [
            -1,
            -1, -1, 3,
            -1, -1, 3, 3, 3
        ],
        [
            -1,
            -1, -1, -1,
            -1, -1, -1, -1, -1
        ],
        [
            -1,
            -1, -1, 0,
            -1, -1, 0, 0, 0 # Yellow is a little bit weird because we flip the shape here...
        ]
    ]

    L_PRIME = [
        [
            -1,
            3, -1, -1,
            3, 3, 3, -1, -1
        ],
        [
            -1,
            -1, -1, 0,
            -1, -1, 0, 0, 0
        ],
        [
            -1,
            -1, -1, -1,
            -1, -1, -1, -1, -1
        ],
        [
            -1,
            -1, -1, 1,
            -1, -1, 1, 1, 1
        ]
    ]

    R = [
        [
            -1,
            -1, -1, 3,
            -1, -1, 3, 3, 3
        ],
        [
            -1,
            -1, -1, -1,
            -1, -1, -1, -1, -1
        ],
        [
            -1,
            0, -1, -1,
            0, 0, 0, -1, -1
        ],
        [
            -1,
            2, -1, 1,
            2, 2, 2, 1, 1
        ]
    ]

    R_PRIME = [
        [
            -1,
            -1, -1, 2,
            -1, -1, 2, 2, 2
        ],
        [
            -1,
            -1, -1, -1,
            -1, -1, -1, -1, -1
        ],
        [
            -1,
            3, -1, -1,
            3, 3, 3, -1, -1
        ],
        [
            -1,
            0, -1, 1,
            0, 0, 0, 1, 1
        ]
    ]

    B = [
        [
            -1,
            -1, -1, -1,
            -1, -1, -1, -1, -1
        ],
        [
            -1,
            2, -1, -1,
            2, 2, 2, -1, -1
        ],
        [
            -1,
            -1, -1, 3,
            -1, -1, 3, 3, 3
        ],
        [
            1,
            1, 1, 1,
            -1, -1, -1, -1, -1
        ]
    ]

    B_PRIME = [
        [
            -1,
            -1, -1, -1,
            -1, -1, -1, -1, -1
        ],
        [
            -1,
            3, -1, -1,
            3, 3, 3, -1, -1
        ],
        [
            -1,
            -1, -1, 1,
            -1, -1, 1, 1, 1
        ],
        [
            2,
            2, 2, 2,
            -1, -1, -1, -1, -1
        ]
    ]

    U = [
        [
            2,
            2, 2, 2,
            -1, -1, -1, -1, -1
        ],
        [
            0,
            0, 0, 0,
            -1, -1, -1, -1, -1
        ],
        [
            1,
            1, 1, 1,
            -1, -1, -1, -1, -1
        ],
        [
            -1,
            -1, -1, -1,
            -1, -1, -1, -1, -1
        ]
    ]

    U_PRIME = [
        [
            1,
            1, 1, 1,
            -1, -1, -1, -1, -1
        ],
        [
            2,
            2, 2, 2,
            -1, -1, -1, -1, -1
        ],
        [
            0,
            0, 0, 0,
            -1, -1, -1, -1, -1
        ],
        [
            -1,
            -1, -1, -1,
            -1, -1, -1, -1, -1
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


class Pyraminx:

    def __init__(self):
        self.sides = [
            ColorSide(Color.GREEN),
            ColorSide(Color.RED),
            ColorSide(Color.BLUE),
            ColorSide(Color.YELLOW)
        ]

        for side in self.sides:
            side.reset()

    def move(self, notation): # execuse me???????????????????????????????????????????????

        copy_sides = self.sides.copy()
        d = copy_sides.copy()

        if notation == "U":

            lmap = MoveMappings.U.value
            print(str(lmap))

            for i in range(len(self.sides)):

                instructions = lmap[i]
                print("instructions:", instructions) # for each side, get instructions how to turn

                real_side = self.sides[i]
                print("current side color:", real_side.color)

                print("I'm a copy of a object, so I won't change value:")

                for l in copy_sides:
                    print(l.piece_side)

                for j in range(len(real_side.piece_side)): # for every piece, copy the value

                    origin_color = instructions[j]

                    print(f"Copying from side with color {origin_color}")

                    if origin_color == -1:
                        continue

                    origin_side = copy_sides[origin_color]
                    print("origin, unchangeable", origin_side.piece_side)
                    print("real:", real_side.piece_side)

                    r = origin_side.piece_side[j]

                    print(f"setting piece {j} with value {real_side.piece_side[j]} to {origin_side.piece_side[j]}")
                    real_side.piece_side[j] = r

                    print("SAME: ", copy_sides == d)


if __name__ == "__main__":
    # for _ in range(5):
    #     print(get_scramble())

    pm = Pyraminx()
    for n, s in enumerate(pm.sides):
        print(s.piece_side, n)
    print("<<b")
    pm.move("U")
    print("moved;")
    for n, s in enumerate(pm.sides):
        print(s.piece_side, n)
    print("<<p")
