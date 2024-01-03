import assets.puzzles.clock.emulator
from assets.puzzles.abstract_puzzle_solver import AbstractPuzzleSolver
from assets.puzzles.abstract_puzzle_emulator import AbstractPuzzleEmulator

class ClockSolver(AbstractPuzzleSolver):

    def __init__(self):
        pass

    def solve(self, puzzle: AbstractPuzzleEmulator) -> (int, str):

        puzzle: assets.puzzles.clock.emulator.ClockEmulator

        optimal_ticks = None
        optimal_solutions = []

        for side in range(2):
            for rotation in range(4):

                res = tommy(puzzle, side, rotation)

                if optimal_ticks is None:
                    optimal_ticks = res[0]
                    optimal_solutions = [res[1]]
                else:
                    if res[0] < optimal_ticks:
                        optimal_ticks = res[0]
                        optimal_solutions = [res[1]]
                    elif res[0] == optimal_ticks:
                        optimal_ticks = res[0]
                        optimal_solutions.append(res[1])

        return optimal_ticks, optimal_solutions


def normalize_notation_move_amount(amount: int):

    amount %= 12

    res = amount

    if res > 6:
        return -(12 - res)

    return res



def absolute_ticks(ticks: int) -> int: # clock 12
    return abs(normalize_notation_move_amount(ticks))


def tommy(puzzle: assets.puzzles.clock.emulator.ClockEmulator, side: int, rotation: int): # side is actually where you start solving from.

    puzzle.rotation = rotation
    puzzle.rotation %= 4

    m1 = (puzzle.get_clock_piece_from_notation(side, "c", "x2")
          - puzzle.get_clock_piece_from_notation(side, "d", "x2"))

    m2 = ((puzzle.get_clock_piece_from_notation(side, "dr", "x2") - puzzle.get_clock_piece_from_notation(side, "r", "x2"))
          + (puzzle.get_clock_piece_from_notation(side, "U", "x2") - puzzle.get_clock_piece_from_notation(side, "L", "x2")))

    m3 = (puzzle.get_clock_piece_from_notation(side, "d", "x2")
          - puzzle.get_clock_piece_from_notation(side, "r", "x2"))

    m4 = (puzzle.get_clock_piece_from_notation(side, "L", "x2")
          - puzzle.get_clock_piece_from_notation(side, "U", "x2"))

    m5 = ((puzzle.get_clock_piece_from_notation(side, "L", "x2")
           - puzzle.get_clock_piece_from_notation(side, "UL", "x2")) - m3)

    m6 = (puzzle.get_clock_piece_from_notation(side, "U", "x2")
          - puzzle.get_clock_piece_from_notation(side, "C", "x2"))

    m7 = -((puzzle.get_clock_piece_from_notation(side, "U", "x2")
          - puzzle.get_clock_piece_from_notation(side, "C", "x2")
           + puzzle.get_clock_piece_from_notation(side, "D", "x2"))

        + (puzzle.get_clock_piece_from_notation(side, "ul", "x2")
           - puzzle.get_clock_piece_from_notation(side, "l", "x2"))

        + (puzzle.get_clock_piece_from_notation(side, "dr", "x2")
           - puzzle.get_clock_piece_from_notation(side, "r", "x2")))

    m8 = ((puzzle.get_clock_piece_from_notation(side, "u", "x2")
           - puzzle.get_clock_piece_from_notation(side, "c", "x2")
           + puzzle.get_clock_piece_from_notation(side, "d", "x2"))

          + (puzzle.get_clock_piece_from_notation(side, "UL", "x2")
             - puzzle.get_clock_piece_from_notation(side, "L", "x2"))

          + (puzzle.get_clock_piece_from_notation(side, "DR", "x2")
             - puzzle.get_clock_piece_from_notation(side, "R", "x2")))

    m9 = (puzzle.get_clock_piece_from_notation(side, "D", "x2")
          - puzzle.get_clock_piece_from_notation(side, "C", "x2"))

    m10 = ((puzzle.get_clock_piece_from_notation(side, "R", "x2") - puzzle.get_clock_piece_from_notation(side, "DR",
                                                                                                         "x2"))
          + (puzzle.get_clock_piece_from_notation(side, "l", "x2") - puzzle.get_clock_piece_from_notation(side, "u",
                                                                                                          "x2")))

    m11 = (puzzle.get_clock_piece_from_notation(side, "R", "x2")
          - puzzle.get_clock_piece_from_notation(side, "D", "x2"))

    m12 = (puzzle.get_clock_piece_from_notation(side, "u", "x2")
          - puzzle.get_clock_piece_from_notation(side, "l", "x2"))

    m13 = ((puzzle.get_clock_piece_from_notation(side, "ul", "x2")
           - puzzle.get_clock_piece_from_notation(side, "l", "x2")) - m11)

    m14 = (puzzle.get_clock_piece_from_notation(side, "c", "x2")
           - puzzle.get_clock_piece_from_notation(side, "u", "x2"))
    
    ticks = 0
    
    for i in range(1, 15):
        m = eval(f"m{i}")
        ticks += absolute_ticks(m)

    solution = f"[LR] "

    if side == 0:
        if rotation == 0:
            solution += "x2 "
        elif rotation == 1:
            solution += "x2 z "
        elif rotation == 2:
            solution += "y2 "
        elif rotation == 3:
            solution += "x2 z' "
    elif side == 1:
        if rotation == 0:
            solution += "z2 "
        elif rotation == 1:
            solution += "z "
        elif rotation == 3:
            solution += "z' "

    solution += (f"dl({normalize_notation_move_amount(m1)}, {normalize_notation_move_amount(m2)}) "
                f"R({normalize_notation_move_amount(m3)}, {normalize_notation_move_amount(m4)}) "
                f"DR({normalize_notation_move_amount(m5)}, {normalize_notation_move_amount(m6)}) "
                f"\\\({normalize_notation_move_amount(m7)}, {normalize_notation_move_amount(m8)}) "
                f"UL({normalize_notation_move_amount(m9)}, {normalize_notation_move_amount(m10)}) "
                f"L({normalize_notation_move_amount(m11)}, {normalize_notation_move_amount(m12)}) "
                f"ur({normalize_notation_move_amount(m13)}, {normalize_notation_move_amount(m14)})")

    solution += "\n[UD] "

    if side == 0:
        if rotation == 0:
            solution += "x2 "
        elif rotation == 1:
            solution += "x2 z "
        elif rotation == 2:
            solution += "y2 "
        elif rotation == 3:
            solution += "x2 z' "
    elif side == 1:
        if rotation == 0:
            solution += "z2 "
        elif rotation == 1:
            solution += "z "
        elif rotation == 3:
            solution += "z' "

    solution += (f"dl({normalize_notation_move_amount(m2)}, {normalize_notation_move_amount(m1)}) "
                 f"R({normalize_notation_move_amount(m4)}, {normalize_notation_move_amount(m3)}) "
                 f"DR({normalize_notation_move_amount(m6)}, {normalize_notation_move_amount(m5)}) "
                 f"\\\({normalize_notation_move_amount(m7)}, {normalize_notation_move_amount(m8)}) "
                 f"UL({normalize_notation_move_amount(m9)}, {normalize_notation_move_amount(m10)}) "
                 f"L({normalize_notation_move_amount(m11)}, {normalize_notation_move_amount(m12)}) "
                 f"ur({normalize_notation_move_amount(m13)}, {normalize_notation_move_amount(m14)})")

    return ticks, solution
    
def bpaul(puzzle: assets.puzzles.clock.emulator.ClockEmulator, side: int, rotation: int):

    puzzle.rotation = rotation
    puzzle.rotation %= 4