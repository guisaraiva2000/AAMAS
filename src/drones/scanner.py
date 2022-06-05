from drones.drone import Drone
from environment.tile import Recharger
from utils.settings import PURPLE, FOV_SCANNER_RANGE
from utils.util import random_direction


class DroneScanner(Drone):
    def __init__(self, clean_waters, x, y):
        super().__init__(clean_waters, x, y, PURPLE)
        self.fov_range = FOV_SCANNER_RANGE

    def agent_decision(self):
        if self.clean_waters.tile_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            self.target_moving()

    def needs_recharge(self):
        return self.battery < 90

    def target_moving(self) -> None:
        self.move(random_direction())
