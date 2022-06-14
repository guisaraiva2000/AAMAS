from drones.drone import Drone
from environment.tile import Recharger
from utils.settings import *
from utils.settings import GREEN, FOV_SCANNER_RANGE
from utils.util import Point, random_direction
from utils.util import Direction

class DroneScanner(Drone):
    def __init__(self, clean_waters, x, y, scanner_id):
        super().__init__(clean_waters, x, y, GREEN)
        self.fov_range = FOV_SCANNER_RANGE
        self.battery = 9999
        self.scanner_id = scanner_id
        self.drone_bounds = self.assign_boundaries()
        
    def assign_boundaries(self):
        if self.scanner_id == 0: #(xmin, xmax, ymin, ymax)
            return [0, 15, 0, 15]
        if self.scanner_id == 1:
            return [16, 31, 0, 15]
        if self.scanner_id == 2:
            return [0, 15, 16, 31]
        if self.scanner_id == 3:
            return [16, 31, 16, 31]
        
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

    def move(self, direction) -> None:
        if direction == -1:
            self.spend_energy()
            self.is_dead()
            self.fov = self.calculate_fov()
            return

        drone_points = []
        for drone in self.clean_waters.drone_list:
            drone_points.append(drone.point)
        
        point = self.point
        if direction == Direction.West and self.point.x > self.drone_bounds[0] and self.point.x > 0:
            point = Point(self.point.x - 1, self.point.y)
        elif direction == Direction.East and self.point.x < self.drone_bounds[1] and self.point.x < 31:
            point = Point(self.point.x + 1, self.point.y)
        elif direction == Direction.South and self.point.y < self.drone_bounds[3] and self.point.y < 31:
            point = Point(self.point.x, self.point.y + 1)
        elif self.point.y >  self.drone_bounds[2] and self.point.y > 0:
            point = Point(self.point.x, self.point.y - 1) 
              
        if point not in drone_points:
            self.point = point
            self.rect.center = [int((self.point.x * TILESIZE) + TILE_MARGIN_X),
                                int((self.point.y * TILESIZE) + TILE_MARGIN_Y)]

        self.spend_energy()
        self.is_dead()
        self.fov = self.calculate_fov()
        return


    def target_moving(self)-> None:
        self.move(random_direction())
         
    def send_oil_alert(self, tile):
        for i in range(len(self.clean_waters.oil_list)):
            if not self.clean_waters.oil_list[i].detected and tile in self.clean_waters.oil_list[i].tiles:
                self.clean_waters.oil_list[i].detected = True
                print("Oil detected in Sector {}".format(tile.sector))
                return
