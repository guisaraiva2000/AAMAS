from drones.drone import Drone
from environment.tile import Recharger
from utils.settings import GREEN, FOV_SCANNER_RANGE
from utils.util import random_direction


class DroneScanner(Drone):
    def __init__(self, clean_waters, x, y):
        super().__init__(clean_waters, x, y, GREEN)
        self.fov_range = FOV_SCANNER_RANGE
        self.battery = 9999

    def agent_decision(self):
        for point in self.fov:
            tile = self.clean_waters.tile_dict[point]
            if tile.with_oil or tile.__class__ == Recharger:
                self.clean_waters.scanned_poi_tiles[point] = tile
                self.send_oil_alert(tile)

        if self.clean_waters.tile_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            self.target_moving()

    def needs_recharge(self):
        return self.battery < 150

    def target_moving(self) -> None:
        self.move(random_direction())

    def send_oil_alert(self, tile):
        for i in range(len(self.clean_waters.oil_list)):
            if not self.clean_waters.oil_list[i].detected and tile in self.clean_waters.oil_list[i].tiles:
                self.clean_waters.oil_list[i].detected = True
                print("Oil detected in Sector {}".format(tile.sector))
                return
