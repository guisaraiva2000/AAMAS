import random
from dataclasses import dataclass, field
from typing import List

from utils.util import Direction, all_directions
from environment.tile import *


@dataclass
class Wind:
    direction: Direction
    strength: int = 10  # Max Intensity


@dataclass(order=True)
class Oil:
    oid: int
    start_location: Point = field(compare=False)
    start_time: int = field(default=1, compare=False)
    points: List[Point] = field(default_factory=list, compare=False)
    tiles: List[Tile] = field(default_factory=list, compare=False)
    stop_time: int = field(default=0, compare=False)
    detected: bool = field(default=False, compare=False)

    def __str__(self):
        return "Oil ID: " + str(self.oid) \
               + "\nStart Location: " + str(self.start_location) \
               + "\nPoints: " + str(len(self.points)) \
               + "\nTiles With Oil: " + str(len(self.tiles))

    def add_oil(self, tile: Tile):
        if tile.point not in self.points:
            self.points.append(tile.point)
            self.tiles.append(tile)

    def update_oil(self) -> None:
        self.tiles = [tile for tile in self.tiles if tile.with_oil]

    def expand_oil(self, tile_dict: dict, wind: Wind) -> None:
        direct = all_directions + (wind.strength - 1) * [wind.direction]
        new_tiles = []

        for tile in self.tiles:
            choice = random.choice(direct)
            if choice == Direction.North:
                if tile.point.y == 0:
                    continue
                new = tile_dict[Point(tile.point.x, tile.point.y - 1)]
            elif choice == Direction.South and tile.point.y:
                if tile.point.y == 31:
                    continue
                new = tile_dict[Point(tile.point.x, tile.point.y + 1)]
            elif choice == Direction.East and tile.point.x < 31:
                if tile.point.x == 31:
                    continue
                new = tile_dict[Point(tile.point.x + 1, tile.point.y)]
            else:
                if tile.point.x == 0:
                    continue
                new = tile_dict[Point(tile.point.x - 1, tile.point.y)]

            if new.with_oil or new.is_recharger:
                continue
            if new.__class__ not in random.choices([Ocean, Recharger], weights=[0.1, 0.9], k=1):
                continue

            new.with_oil = True
            new_tiles.append(new)

        for oil_spill in new_tiles:
            self.add_oil(oil_spill)
