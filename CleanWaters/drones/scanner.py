from drones.drone import Drone
from environment.square import Recharger
from utils.settings import DARK_BLUE, FOV_SCANNER_RANGE
from utils.util import random_direction


class DroneScanner(Drone):
    def __init__(self, clean_waters, x, y, scanner_id):
        super().__init__(clean_waters, x, y, DARK_BLUE)
        self.fov_range = FOV_SCANNER_RANGE
        self.battery = 9999
        self.scanner_id = scanner_id
        self.drone_bounds = self.assign_boundaries()

    def assign_boundaries(self):
        if self.scanner_id == 0:  # (xmin, xmax, ymin, ymax)
            return [0, 15, 0, 15]
        if self.scanner_id == 1:
            return [16, 31, 0, 15]
        if self.scanner_id == 2:
            return [0, 15, 16, 31]
        if self.scanner_id == 3:
            return [16, 31, 16, 31]

    def agent_decision(self):
        for point in self.fov:
            square = self.clean_waters.square_dict[point]
            if square.with_oil or square.__class__ == Recharger:
                self.clean_waters.scanned_poi_squares[point] = square
                self.send_oil_alert(square)

        if self.clean_waters.square_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            self.move(random_direction(), self.drone_bounds)

    def needs_recharge(self):
        return self.battery < 150

    def send_oil_alert(self, square):
        for i in range(len(self.clean_waters.oil_list)):
            if not self.clean_waters.oil_list[i].detected and square in self.clean_waters.oil_list[i].squares:
                self.clean_waters.oil_list[i].detected = True
                print("Oil detected in Zone {}".format(square.zone))
                return
