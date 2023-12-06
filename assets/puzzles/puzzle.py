from assets.puzzles.abstract_puzzle import AbstractPuzzle


def load_puzzle(puzzle: str) -> AbstractPuzzle:
    exec(f'import assets.puzzles.{puzzle}.puzzle')
    p = eval(f'assets.puzzles.{puzzle}.puzzle.{puzzle[0].upper() + puzzle[1:]}()')
    return p
