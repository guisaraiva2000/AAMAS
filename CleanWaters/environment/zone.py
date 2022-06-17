from utils.util import Point
from typing import List


class Zone:
    def __init__(self, clean_waters, zone_id, zone_height, zone_width):
        self.clean_waters = clean_waters
        self.zone_id = zone_id
        self.zone_height = zone_height
        self.zone_width = zone_width
        self.zone_points: List[Point] = []

    def create_zone(self, left_corner_x: int, left_corner_y: int):
        for y in range(left_corner_y, left_corner_y + self.zone_height, 1):
            for x in range(left_corner_x, left_corner_x + self.zone_width, 1):
                point = Point(x, y)
                self.zone_points.append(point)
                self.clean_waters.square_dict[point].zone = self.zone_id
