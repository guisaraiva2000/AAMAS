import random
from dataclasses import dataclass, field
from utils.util import Direction
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

    def __str__(self):
        return "Oil ID: " + str(self.oid) \
               + "\nStart Location: " + str(self.start_location) \
               + "\nPoints: " + str(len(self.points)) \
               + "\nTiles With Oil: " + str(len(self.tiles))

    def add_oil(self, tile: Tile):
        if tile.point not in self.points:
            self.points.append(tile.point)
            self.tiles.append(tile)


def update_oil(oil: Oil) -> None:
    oil.tiles = [tile for tile in oil.tiles if tile.with_oil]


def expand_oil(oil: Oil, tile_dict: dict, wind: Wind) -> None:
    direct = [Direction.North, Direction.South, Direction.East, Direction.West] + (wind.strength - 1) * [wind.direction]
    types = [Ocean, Recharger]
    new_tiles = []

    for tile in oil.tiles:
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
        if new.__class__ not in random.choices(types, weights=[0.3, 0.7], k=1):
            continue

        new.with_oil = True
        new_tiles.append(new)

    for oil_spill in new_tiles:
        oil.add_oil(oil_spill)
