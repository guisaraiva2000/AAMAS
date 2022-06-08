import pygame
from utils.util import Point
from utils.settings import *
from abc import ABC


class Tile(pygame.sprite.Sprite, ABC):
    def __init__(self, clean_waters, x, y, color):
        super().__init__()
        self.clean_waters = clean_waters
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.point = Point(x, y)
        self.with_oil = False
        self.is_recharger = False
        self.sector = None
        self.rect.center = [int((x * TILESIZE) + TILE_MARGIN_X), int((y * TILESIZE) + TILE_MARGIN_Y)]

    def __repr__(self):
        return f"Class:{self.__class__}, {self.point}, With Oil:{self.with_oil}"


class Recharger(Tile):
    def __init__(self, clean_waters, x, y):
        super().__init__(clean_waters, x, y, RED)
        self.is_recharger = True


class Ocean(Tile):
    def __init__(self, clean_waters, x, y):
        super().__init__(clean_waters, x, y, BLUE)
