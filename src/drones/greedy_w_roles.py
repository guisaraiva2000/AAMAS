import random
import numpy as np
from drones.drone import Drone
from environment.tile import Recharger, Tile
from utils.settings import FOV_CLEANER_RANGE, YELLOW
from utils.util import give_directions, is_oil_scanned, Point, all_directions, random_direction
from typing import List


class DroneGreedyRoles(Drone):
    def __init__(self, clean_waters, x, y, drone_id):
        super().__init__(clean_waters, x, y, YELLOW)
        self.fov_range = FOV_CLEANER_RANGE
        self.role = None
        self.drone_id = drone_id

    def role_assignment(self):
        def potential_function(drone_point: Point, oil_tiles: List[Tile]) -> float:
            closest_point = drone_point.closest_point_from_points([oil_tile.point for oil_tile in oil_tiles])
            return -drone_point.distance_to(closest_point)

        oil_spills = [oil for oil in self.clean_waters.oil_list
                      if not oil.stop_time and is_oil_scanned(oil.tiles, self.clean_waters.scanned_poi_tiles, self.fov)]
        n_oil_spills = len(oil_spills)
        drone_list = [drone for drone in self.clean_waters.drone_list if drone.__class__ == self.__class__]
        n_drones = len(drone_list)

        if n_oil_spills and n_drones:
            # Calculate potentials for all drones and roles (oil spill).
            potentials = np.zeros((n_oil_spills, n_drones))
            for oil_idx in range(n_oil_spills):
                for drone in range(n_drones):
                    potentials[oil_idx, drone] = potential_function(drone_list[drone].point, oil_spills[oil_idx].tiles)

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
            self.target_moving()
            self.role = None

        return

    def needs_recharge(self) -> bool:
        return self.battery <= 150

    def target_moving(self) -> None:
        direction_lists = poi = [[], []]
        drones_around = self.see_drones_around()
        scanned_poi = list(self.clean_waters.scanned_poi_tiles.keys())
        observed_points = scanned_poi + self.fov if scanned_poi else self.fov

        if self.role:
            for point in observed_points:
                if point in self.role.points and self.clean_waters.tile_dict[point].with_oil:
                    poi[1].append(point)

                elif self.clean_waters.tile_dict[point].__class__ == Recharger and self.needs_recharge():
                    poi[0].append(point)

            if poi[0]:
                direction_lists[0] = give_directions(self.point, [self.point.closest_point_from_points(poi[0])])
            if poi[1]:
                direction_lists[1] = give_directions(self.point, [self.point.closest_point_from_points(poi[1])])

            for direction_list in direction_lists:
                dirs = [d for d in direction_list if d not in give_directions(self.point, drones_around)]
                if dirs:
                    self.move(random.choice(dirs))
                    return

        not_poi = [d for d in all_directions if d not in give_directions(self.point, drones_around)]
        self.move(random_direction()) if not_poi else self.move(-1)
