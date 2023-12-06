from abc import ABC, abstractmethod
from assets.puzzles.abstract_puzzle_renderer import AbstractPuzzleRenderer
from assets.puzzles.abstract_puzzle_scrambler import AbstractPuzzleScrambler
from assets.puzzles.abstract_puzzle_emulator import AbstractPuzzleEmulator


class AbstractPuzzle(ABC):
    _renderer: AbstractPuzzleRenderer
    _scrambler: AbstractPuzzleScrambler
    _emulator: AbstractPuzzleEmulator

    @abstractmethod
    def __init__(self):
        pass

    @property
    def renderer(self) -> AbstractPuzzleRenderer:
        return self._renderer

    @property
    def scrambler(self) -> AbstractPuzzleScrambler:
        return self._scrambler

    @property
    def emulator(self) -> AbstractPuzzleEmulator:
        return self._emulator
