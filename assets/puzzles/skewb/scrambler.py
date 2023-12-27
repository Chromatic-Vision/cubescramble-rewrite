import random
from assets.puzzles.abstract_puzzle_scrambler import AbstractPuzzleScrambler

class SkewbScrambler(AbstractPuzzleScrambler):
    def __init__(self):
        pass

    def get_random_scramble(self) -> str: # lol really similar to pyraminx
        rm = []

        for i in range(9):
            move = random_move()

            if len(rm) > 0:  # if the scramble is not empty, check if the next base move equals to the previous one
                while get_base_of_move(move) == get_base_of_move(rm[i - 1]):
                    move = random_move()

            rm.append(move)

        scramble = " ".join(rm)

        return scramble


MOVES = ["L", "R", "B", "U"]

def random_move():
    return random.choice(MOVES) + prime_random()

def prime_random():
    return "'" if bool(random.getrandbits(1)) else ""

def get_base_of_move(move: str):
    res = move
    res = res.replace(" ", "") # remove space
    res = res.replace("'", "") # remove prime

    return res

if __name__ == "__main__":
    c = SkewbScrambler()
    for _ in range(10):
        print(c.get_random_scramble())