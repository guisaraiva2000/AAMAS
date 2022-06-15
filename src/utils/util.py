import math
import random
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    North = 1
    South = 2
    East = 3
    West = 4


all_directions = [Direction.North, Direction.South, Direction.East, Direction.West]


@dataclass(order=True, repr=True, frozen=True)
class Point:
    x: int
    y: int

    def distance_to(self, to_point):
        return math.dist((self.x, self.y), (to_point.x, to_point.y))

    def closest_point_from_points(self, points):
        return min(points, key=lambda point: self.distance_to(point))


def random_direction():
    return random.choice(all_directions)


def give_directions(curr_point, ps: list) -> list:
    directions = []
    for p in ps:
        if len(directions) == 4:
            break
        if p.x < curr_point.x and Direction.West not in directions:
            directions.append(Direction.West)
        if p.x > curr_point.x and Direction.East not in directions:
            directions.append(Direction.East)
        if p.y > curr_point.y and Direction.South not in directions:
            directions.append(Direction.South)
        if p.y < curr_point.y and Direction.North not in directions:
            directions.append(Direction.North)
    return directions


def is_oil_scanned(oil_spill_tiles, scanned_oil_spills_dict, drone_fov):
    for oil_tile in oil_spill_tiles:
        if oil_tile in scanned_oil_spills_dict.values() or oil_tile.point in drone_fov:
            return True
    return False
