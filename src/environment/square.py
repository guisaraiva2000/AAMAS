import pygame
from utils.util import Point
from utils.settings import *
from abc import ABC


class Square(pygame.sprite.Sprite, ABC):
    def __init__(self, clean_waters, x, y, color):
        super().__init__()
        self.clean_waters = clean_waters
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.point = Point(x, y)
        self.with_oil = False
        self.is_recharger = False
        self.zone = None
        self.rect.center = [int((x * SQUARE_SIZE) + SQUARE_MARGIN_X), int((y * SQUARE_SIZE) + SQUARE_MARGIN_Y)]

    def __repr__(self):
        return f"Class:{self.__class__}, {self.point}, With Oil:{self.with_oil}"


class Recharger(Square):
    def __init__(self, clean_waters, x, y):
        super().__init__(clean_waters, x, y, RED_WINE)
        self.is_recharger = True


class Ocean(Square):
    def __init__(self, clean_waters, x, y):
        super().__init__(clean_waters, x, y, BLUE)
