from drones.drone import Drone
from environment.tile import Recharger
from utils.util import random_direction


class DroneRandom(Drone):
    def __init__(self, simulation, x, y):
        super().__init__(simulation, x, y)

    def agent_decision(self):
        if self.simulation.tile_dict[self.point].with_oil:
            self.clean_water()

        elif self.simulation.tile_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            self.target_moving()

    def needs_recharge(self):
        return self.battery < 90

    def target_moving(self) -> None:
        self.move(random_direction())
