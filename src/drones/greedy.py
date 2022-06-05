from drones.drone import Drone
import random
from utils.settings import FOV_CLEANER_RANGE, YELLOW
from environment.tile import Recharger
from utils.util import Direction, random_direction


class DroneGreedy(Drone):
    def __init__(self, clean_waters, x, y):
        super().__init__(clean_waters, x, y, YELLOW)
        self.fov_range = FOV_CLEANER_RANGE

    def agent_decision(self) -> None:
        if self.clean_waters.tile_dict[self.point].with_oil:
            self.clean_water()

        elif self.clean_waters.tile_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            self.target_moving()
        return

    def needs_recharge(self) -> bool:
        return self.battery <= 50

    def target_moving(self) -> None:
        self.reactive_movement()
