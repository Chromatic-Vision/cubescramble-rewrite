from assets.puzzles.abstract_puzzle import AbstractPuzzle

def load_puzzle(puzzle: str) -> AbstractPuzzle:
    import assets.puzzles.clock.puzzle
    import assets.puzzles.pyraminx.puzzle
    p = eval(f'assets.puzzles.{puzzle}.puzzle.{puzzle[0].upper() + puzzle[1:]}()')
    return p

PUZZLES = [
    "clock",
    "pyraminx"
]