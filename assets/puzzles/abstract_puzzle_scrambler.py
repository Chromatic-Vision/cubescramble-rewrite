from abc import ABC, abstractmethod


class AbstractPuzzleScrambler(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_random_scramble(self) -> str:
        pass
