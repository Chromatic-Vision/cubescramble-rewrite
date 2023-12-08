from assets.puzzles.abstract_puzzle import AbstractPuzzle
from assets.puzzles.clock.emulator import ClockEmulator
from assets.puzzles.clock.scrambler import ClockScrambler
from assets.puzzles.clock.renderer import ClockRenderer


class Clock(AbstractPuzzle):
    def __init__(self):
        self._scrambler = ClockScrambler()
        self._emulator: ClockEmulator = ClockEmulator()
        self._renderer = ClockRenderer(self._emulator)

    @property
    def scrambler(self):
        return self._scrambler
