import random
import numpy as np
from drones.drone import Drone
from environment.tile import Recharger
from utils.settings import FOV_CLEANER_RANGE, YELLOW
from utils.util import give_directions, is_oil_scanned, potential_function


class DroneGreedyRoles(Drone):
    def __init__(self, clean_waters, x, y, drone_id):
        super().__init__(clean_waters, x, y, YELLOW)
        self.fov_range = FOV_CLEANER_RANGE
        self.role = None
        self.drone_id = drone_id
        self.selected_point1 = None


    def role_assignment(self):
        oil_spills = [oil for oil in self.clean_waters.oil_list
                      if not oil.stop_time and is_oil_scanned(oil.points, self.clean_waters.scanned_poi_tiles, self.fov)]
        oil_spills.reverse()
        n_oil_spills = len(oil_spills)
        drone_list = [drone for drone in self.clean_waters.drone_list if drone.__class__ == self.__class__]
        n_drones = len(drone_list)

        if n_oil_spills and n_drones:
            # Calculate potentials for all drones and roles (oil spill).
            potentials = np.zeros((n_oil_spills, n_drones))
            for oil_idx in range(n_oil_spills):
                for drone in range(n_drones):
                    potentials[oil_idx, drone] = potential_function(drone_list[drone].point, oil_spills[oil_idx].points)

            drone_roles = {}
            for oil_idx in range(n_oil_spills):
                n_split_drones = n_drones // n_oil_spills
                n_split_drones = 1 if n_split_drones == 0 else n_split_drones
                closest_drones = np.argpartition(potentials[oil_idx], -n_split_drones)[-n_split_drones:]
                for drone in closest_drones:
                    drone_roles[drone_list[drone]] = oil_spills[oil_idx]
                    potentials[:, drone] = -999

            return drone_roles

    def agent_decision(self) -> None:
        if self.clean_waters.tile_dict[self.point].with_oil:
            self.clean_water()

        elif self.clean_waters.tile_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            role_assignments = self.role_assignment()
            if role_assignments is not None and self in role_assignments:
                self.role = role_assignments[self]
            elif self.role is not None:
                self.role = None

            self.target_moving()
        return

    def needs_recharge(self) -> bool:
        return self.battery <= 150

    def target_moving(self) -> None:
        drones_around = self.see_drones_around()

        if self.role is not None and self.selected_point is None:
            oil_points = [oil for oil in self.role.points
                          if oil in self.clean_waters.scanned_poi_tiles or oil in self.fov]
            self.selected_point1 = [self.point.closest_point_from_points(oil_points)]
            dir_list = give_directions(self.point, self.selected_point1)
            dirs = [d for d in dir_list if d not in give_directions(self.point, drones_around)]
            if dirs:
                self.move(random.choice(dirs))
                return
        if self.point == self.selected_point:
            self.selected_point1 = None
        self.reactive_movement()
