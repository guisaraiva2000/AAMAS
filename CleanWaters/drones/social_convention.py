from drones.drone import Drone
from environment.square import Recharger
from utils.settings import FOV_CLEANER_RANGE, YELLOW


class DroneSocialConvention(Drone):
    def __init__(self, clean_waters, x, y, drone_id):
        super().__init__(clean_waters, x, y, YELLOW)
        self.fov_range = FOV_CLEANER_RANGE
        self.role = None
        self.drone_id = drone_id
        self.drone_bounds = self.assign_boundaries()
        self.drone_zones = self.assign_zones()
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

    def assign_zones(self):
        if self.drone_id == 0:
            return [0, 2]
        if self.drone_id == 1:
            return [1, 3]
        if self.drone_id == 2:
            return [4, 6]
        if self.drone_id == 3:
            return [5, 7]
        if self.drone_id == 4:
            return [2, 4]
        if self.drone_id == 5:
            return [3, 5]

    def agent_decision(self) -> None:
        if self.clean_waters.square_dict[self.point].with_oil:
            self.clean_water()

        elif self.clean_waters.square_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            self.movement(self.drone_bounds, self.drone_zones)

    def needs_recharge(self) -> bool:
        return self.battery <= 150
