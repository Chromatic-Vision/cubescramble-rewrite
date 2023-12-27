import random
from assets.puzzles.abstract_puzzle_scrambler import AbstractPuzzleScrambler

class Sq1Scrambler(AbstractPuzzleScrambler):
    def __init__(self):
        pass

    def get_random_scramble(self) -> str: # TODO: make this work

        moves = [random_move() for _ in range(random.randint(11, 13))]
        scramble = "/ ".join(moves)

        return scramble

def random_move():
    return f"({random.randint(-5, 6)}, {random.randint(-5, 6)})"

if __name__ == "__main__":
    c = Sq1Scrambler()

    for _ in range(100):
        print(c.get_random_scramble())