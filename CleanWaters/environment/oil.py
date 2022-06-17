import random
from dataclasses import dataclass, field
from typing import List

from utils.util import Direction, all_directions
from environment.square import *


@dataclass
class Wind:
    direction: Direction
    strength: int = MAX_WIND  # Max Intensity


@dataclass(order=True)
class Oil:
    oid: int
    start_location: Point = field(compare=False)
    start_time: int = field(default=1, compare=False)
    points: List[Point] = field(default_factory=list, compare=False)
    squares: List[Square] = field(default_factory=list, compare=False)
    stop_time: int = field(default=0, compare=False)
    detected: bool = field(default=False, compare=False)

    def __str__(self):
        return "Oil ID: " + str(self.oid) \
               + "\nStart Location: " + str(self.start_location) \
               + "\nPoints: " + str(len(self.points)) \
               + "\nSquares With Oil: " + str(len(self.squares))

    def add_oil(self, square: Square):
        if square.point not in self.points:
            self.points.append(square.point)
        self.squares.append(square)

    def update_oil(self) -> None:
        self.squares = [square for square in self.squares if square.with_oil]

    def expand_oil(self, square_dict: dict, wind: Wind) -> None:
        direct = all_directions + (wind.strength - 1) * [wind.direction]
        new_squares = []

        for square in self.squares:
            choice = random.choice(direct)
            if choice == Direction.North:
                if square.point.y == 0:
                    continue
                new = square_dict[Point(square.point.x, square.point.y - 1)]
            elif choice == Direction.South and square.point.y:
                if square.point.y == 31:
                    continue
                new = square_dict[Point(square.point.x, square.point.y + 1)]
            elif choice == Direction.East and square.point.x < 31:
                if square.point.x == 31:
                    continue
                new = square_dict[Point(square.point.x + 1, square.point.y)]
            else:
                if square.point.x == 0:
                    continue
                new = square_dict[Point(square.point.x - 1, square.point.y)]

            if new.with_oil or new.is_recharger:
                continue
            if new.__class__ not in random.choices([Ocean, Recharger], weights=[0.1, 0.9], k=1):
                continue

            new.with_oil = True
            new_squares.append(new)

        for oil_spill in new_squares:
            self.add_oil(oil_spill)
