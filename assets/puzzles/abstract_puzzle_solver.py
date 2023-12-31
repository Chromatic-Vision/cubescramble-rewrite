from abc import ABC, abstractmethod
from assets.puzzles.abstract_puzzle_emulator import AbstractPuzzleEmulator


# e.g. Clock7SimulSolver
class AbstractPuzzleSolver(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def solve(self, puzzle: AbstractPuzzleEmulator) -> (int, str): # optimal moves and solution
        pass
