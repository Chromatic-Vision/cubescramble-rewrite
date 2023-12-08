import random
from assets.puzzles.abstract_puzzle_scrambler import AbstractPuzzleScrambler


class ClockScrambler(AbstractPuzzleScrambler):
    def __init__(self):
        pass

    def get_random_scramble(self) -> str:
        movements = [
            [
                'UR', 'DR', 'DL', 'UL',
                'U', 'R', 'D', 'L', 'ALL'
            ],
            [
                'U', 'R', 'D', 'L'
            ]
        ]

        scramble = " y2 ".join(
            [" ".join(
                [
                    movement + _random_rotation()
                    for movement in movements[i]]
            ) for i in range(2)]
        )
        scramble += _random_pins()

        return scramble


def _random_rotation():
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


def _random_pins():
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


if __name__ == '__main__':
    s = ClockScrambler()
    print(s.get_random_scramble())
