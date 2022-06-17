from drones.drone import Drone
from environment.square import Recharger
from utils.settings import YELLOW
from utils.util import random_direction


class DroneRandom(Drone):
    def __init__(self, clean_waters, x, y):
        super().__init__(clean_waters, x, y, YELLOW)

    def agent_decision(self):
        if self.clean_waters.square_dict[self.point].with_oil:
            self.clean_water()

        elif self.clean_waters.square_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            self.move(random_direction())

    def needs_recharge(self):
        return self.battery < 90
