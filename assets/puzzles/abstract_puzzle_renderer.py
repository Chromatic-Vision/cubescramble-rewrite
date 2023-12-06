from abc import ABC, abstractmethod
import pygame


class AbstractPuzzleRenderer(ABC):
    @abstractmethod
    def __init__(self, puzzle):
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface, pos: pygame.Rect) -> None:
        pass
