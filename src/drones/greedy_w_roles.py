import numpy as np

from drones.drone import Drone
import random

from environment.sector import Sector
from environment.tile import Recharger
from utils.settings import FOV_CLEANER_RANGE, YELLOW
from utils.util import Direction, random_direction, Point, give_directions


class DroneGreedyRoles(Drone):
    def __init__(self, clean_waters, x, y, drone_id):
        super().__init__(clean_waters, x, y, YELLOW)
        self.fov_range = FOV_CLEANER_RANGE
        self.role = None
        self.drone_id = drone_id

    def potential_function(self, drone_point: Point, sector: int, sector_list: list) -> int:
        sector_points_w_oil = [point for point in sector_list[sector].sectorPoints
                               if self.clean_waters.tile_dict[point].with_oil]
        closest_point = drone_point.closest_point_from_points(sector_points_w_oil)
        return -drone_point.distance_to(closest_point)

    def role_assignment(self):
        sector_list = [sector for sector in self.clean_waters.sector_list if sector.has_oil(self.clean_waters.tile_dict)]
        n_sectors = len(sector_list)
        drone_list = self.clean_waters.drone_list
        n_drones = len(drone_list)

        if sector_list:
            # Calculate potentials for all drones and roles (sectors).
            potentials = np.zeros((n_drones, n_sectors))
            for drone in range(n_drones):
                for sector_id in range(n_sectors):
                    potentials[drone, sector_id] = self.potential_function(drone_list[drone].point, sector_id,
                                                                           sector_list)

            drone_roles = np.zeros(n_drones, dtype=Sector)
            for drone in range(n_drones):
                sector_id = np.argmax(potentials[drone])
                drone_roles[drone] = sector_list[sector_id]

            return drone_roles

    def agent_decision(self) -> None:
        if self.clean_waters.tile_dict[self.point].with_oil:
            self.clean_water()

        elif self.clean_waters.tile_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            role_assignments = self.role_assignment()
            if role_assignments is not None:
                self.role = role_assignments[self.drone_id]
            self.target_moving()
        return

    def needs_recharge(self) -> bool:
        return self.battery <= 50

    def target_moving(self) -> None:
        drones_around = self.see_drones_around()

        if self.role is not None:
            sector_points_w_oil = [point for point in self.role.sectorPoints
                                   if self.clean_waters.tile_dict[point].with_oil]
            if sector_points_w_oil and self.point not in sector_points_w_oil:
                dir_list = give_directions(self.point, [self.point.closest_point_from_points(sector_points_w_oil)])
                dirs = [d for d in dir_list if d not in give_directions(self.point, drones_around)]
                if dirs:
                    self.move(random.choice(dirs))
                    return

        self.reactive_movement()
