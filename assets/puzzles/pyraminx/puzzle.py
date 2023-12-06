from assets.puzzles.abstract_puzzle import AbstractPuzzle
from assets.puzzles.pyraminx.scrambler import PyraminxScrambler
from assets.puzzles.pyraminx.emulator import PyraminxEmulator
from assets.puzzles.pyraminx.renderer import PyraminxRenderer


class Pyraminx(AbstractPuzzle):
    def __init__(self):
        self._scrambler = PyraminxScrambler()
        self._emulator: PyraminxEmulator = PyraminxEmulator()
        self._renderer = PyraminxRenderer(self._emulator)
