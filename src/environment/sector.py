from utils.util import Point
from typing import List


class Sector:
    def __init__(self, clean_waters, sector_id, sector_height, sector_width):
        self.clean_waters = clean_waters
        self.sector_id = sector_id
        self.sector_height = sector_height
        self.sector_width = sector_width
        self.sector_points: List[Point] = []

    def create_sector(self, left_corner_x: int, left_corner_y: int):
        for y in range(left_corner_y, left_corner_y + self.sector_height, 1):
            for x in range(left_corner_x, left_corner_x + self.sector_width, 1):
                point = Point(x, y)
                self.sector_points.append(point)
                self.clean_waters.tile_dict[point].sector = self.sector_id

