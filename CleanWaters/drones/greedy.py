from drones.drone import Drone
from utils.settings import FOV_CLEANER_RANGE, YELLOW
from environment.square import Recharger


class DroneGreedy(Drone):
    def __init__(self, clean_waters, x, y):
        super().__init__(clean_waters, x, y, YELLOW)
        self.fov_range = FOV_CLEANER_RANGE

    def agent_decision(self) -> None:
        if self.clean_waters.square_dict[self.point].with_oil:
            self.clean_water()

        elif self.clean_waters.square_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            self.movement()

        return

    def needs_recharge(self) -> bool:
        return self.battery <= 150
