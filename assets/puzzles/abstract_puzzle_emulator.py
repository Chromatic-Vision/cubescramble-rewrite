from abc import ABC, abstractmethod


class AbstractPuzzleEmulator(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def move(self, s: str) -> None:
        pass

    @abstractmethod
    def convert_scramble(self, scramble: str) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass
