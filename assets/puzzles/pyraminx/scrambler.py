from assets.puzzles.abstract_puzzle_scrambler import AbstractPuzzleScrambler
from assets.puzzles.pyraminx.emulator import get_base_of_move
import random


class PyraminxScrambler(AbstractPuzzleScrambler):
    def __init__(self):
        pass

    def get_random_scramble(self) -> str:
        rm = []

        for i in range(8):
            move = random_move()

            if len(rm) > 0: # if the scramble is not empty, check if the next base move equals to the previous one
                while get_base_of_move(move) == get_base_of_move(rm[i - 1]):
                    move = random_move()

            rm.append(move)

        scramble = " ".join(rm) + random_tips()

        return scramble


MOVES = ["L", "R", "B", "U"]


def random_move():
    return random.choice(MOVES) + prime_random()


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
    return "'" if bool(random.getrandbits(1)) else ""