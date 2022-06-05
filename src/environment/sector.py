from dataclasses import dataclass, field
from utils.util import Point
from typing import List
import random


@dataclass(order=True, repr=True)
class Sector:
    sectorID: int
    probabilityPerOilTile: float = field(compare=False)
    sectorSize: int = field(compare=False)
    sectorPoints: List[Point] = field(default_factory=list, compare=False)
    withOil: bool = field(default=False, compare=False)

    def create_sector(self, left_corner_x: int, left_corner_y: int):
        for y in range(left_corner_y, left_corner_y + self.sectorSize, 1):
            for x in range(left_corner_x, left_corner_x + self.sectorSize, 1):
                self.sectorPoints.append(Point(x, y))

    def calculate_oil_alert(self, oil_list):
        final_probability = 0
        total_oil = 0
        for oil in oil_list:
            for oilTile in oil.tiles:
                if oilTile.point in self.sectorPoints:
                    total_oil += 1
                    final_probability += self.probabilityPerOilTile

        # if the sector finds no oil in its tiles
        if not total_oil:
            self.withOil = False
            return False

        # if we already know the sector is with oil
        # we only alert the first occurrence of finding oil
        if self.withOil:
            return False

        # random.random() return a number in interval [0,1[
        self.withOil = random.random() < final_probability
        return self.withOil

    def has_oil(self, tiles: dict):
        for point in self.sectorPoints:
            if tiles[point].with_oil:
                return True
        return False

