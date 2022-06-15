from drones.drone import Drone
from environment.tile import Recharger
from utils.settings import FOV_CLEANER_RANGE, YELLOW

""" 0 -> 0 1 4 5
    1 -> 2 3 6 7
    2 -> 8 9 12 13
    3 -> 10 11 14 15 """


class DroneSocialConvention(Drone):
    def __init__(self, clean_waters, x, y, drone_id):
        super().__init__(clean_waters, x, y, YELLOW)
        self.fov_range = FOV_CLEANER_RANGE
        self.role = None
        self.drone_id = drone_id
        self.drone_bounds = self.assign_boundaries()
        self.drone_sectors = self.assign_sectors()
        self.selected_point = None

    def assign_boundaries(self):
        if self.drone_id == 0:  # (xmin, xmax, ymin, ymax)
            return [0, 15, 0, 15]
        if self.drone_id == 1:
            return [16, 31, 0, 15]
        if self.drone_id == 2:
            return [0, 15, 16, 31]
        if self.drone_id == 3:
            return [16, 31, 16, 31]
        if self.drone_id == 4:
            return [0, 15, 8, 23]
        if self.drone_id == 5:
            return [16, 31, 8, 23]

    def assign_sectors(self):
        if self.drone_id == 0:
            return [0, 1, 4, 5]
        if self.drone_id == 1:
            return [2, 3, 6, 7]
        if self.drone_id == 2:
            return [8, 9, 12, 13]
        if self.drone_id == 3:
            return [10, 11, 14, 15]
        if self.drone_id == 4:
            return [4, 5, 8, 9]
        if self.drone_id == 5:
            return [6, 7, 10, 11]

    def agent_decision(self) -> None:
        if self.clean_waters.tile_dict[self.point].with_oil:
            self.clean_water()

        elif self.clean_waters.tile_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            self.target_moving()

    def needs_recharge(self) -> bool:
        return self.battery <= 150

    def target_moving(self) -> None:
        self.reactive_movement(self.drone_bounds, self.drone_sectors)
