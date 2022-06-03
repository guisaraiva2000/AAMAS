import pygame
from utils.util import Point
from typing import List
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
        self.sector = 0
        self.with_oil = False
        self.is_recharger = False
        self.path_able = True
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


def get_neighbours(tile: Tile, tile_dict: dict) -> List[Tile]:
    lst = []

    p = Point(tile.point.x + 1, tile.point.y)
    if p in tile_dict.keys():
        lst.append(tile_dict[p])

    p = Point(tile.point.x - 1, tile.point.y)
    if p in tile_dict.keys():
        lst.append(tile_dict[p])

    p = Point(tile.point.x, tile.point.y + 1)
    if p in tile_dict.keys():
        lst.append(tile_dict[p])

    p = Point(tile.point.x, tile.point.y - 1)
    if p in tile_dict.keys():
        lst.append(tile_dict[p])
    return lst
