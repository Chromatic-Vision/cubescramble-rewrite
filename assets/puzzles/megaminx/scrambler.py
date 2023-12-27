import random
from assets.puzzles.abstract_puzzle_scrambler import AbstractPuzzleScrambler

class MegaminxScrambler(AbstractPuzzleScrambler):

    def __init__(self):
        pass

    def get_random_scramble(self) -> str:

        scramble = ""

        for o in range(6):

            for i in range(10):

                scramble += BASE_MOVES[i % 2] + random_direction() + " "

            scramble += random_end() + " \n"


        return scramble

def prime_random():
    return "'" if bool(random.getrandbits(1)) else ""

def random_end():
    return "U" + prime_random()

def random_direction():
    return "++" if random.getrandbits(1) else "--"


BASE_MOVES = ["R", "D"]
# END_MOVES = ["U"]