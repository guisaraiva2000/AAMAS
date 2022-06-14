import random
import numpy as np
from drones.drone import Drone
from environment.tile import Recharger
from utils.settings import FOV_CLEANER_RANGE, YELLOW
from utils.util import give_directions, is_oil_scanned, all_directions, random_direction

""" 0 -> 0 1 4 5
    1 -> 2 3 6 7
    2 -> 8 9 12 13
    3 -> 10 11 14 15 """
class DroneSocialConvention(Drone):
    def __init__(self, clean_waters, x, y, drone_id):      
        super().__init__(clean_waters, x, y, YELLOW)
        self.fov_range = FOV_CLEANER_RANGE
        self.role = None
        self.drone_id = drone_id
        self.drone_sectors = self.assign_sectors()
        
    def assign_sectors(self):
        if self.drone_id == 0:
            return [0, 1, 4, 5]
        if self.drone_id == 1:
            return [2, 3, 6, 7]
        if self.drone_id == 2:
            return [8, 9, 12, 13]
        if self.drone_id == 3:
            return [10, 11, 14, 15]
        if self.drone_id == 4:
            return [4, 5, 8, 9]
        if self.drone_id == 5:
            return [6, 7, 10, 11]
        
    def role_assignment(self):

                    
        oil_spills = [oil for oil in self.clean_waters.oil_list
                      if len(oil.tiles) and is_oil_scanned(oil.points, self.clean_waters.scanned_poi_tiles, self.fov)]
        
        #n_oil_spills = len(oil_spills)
        for oil in oil_spills:
            #print("oil tile", oil.tiles)
            for tile in oil.tiles:
               # print("oil sector", tile.sector, "drone sectors", self.drone_sectors)  
                if tile.sector in self.drone_sectors:
                    #print("found")           
                    return oil
        """drone_list = [drone for drone in self.clean_waters.drone_list if drone.__class__ == self.__class__]
        n_drones = len(drone_list)

        if n_oil_spills:
            # Calculate potentials for all drones and roles (oil spill).
            potentials = np.zeros((n_oil_spills, n_drones))
            for oil_idx in range(n_oil_spills):
                for drone in range(n_drones):
                    potentials[oil_idx, drone] = potential_function(drone_list[drone].point, oil_spills[oil_idx].points)

            
            for oil_idx in range(n_oil_spills):
                n_split_drones = n_drones // n_oil_spills
                closest_drones = np.argpartition(potentials[oil_idx], -n_split_drones)[-n_split_drones:]
                for drone in closest_drones:
                    drone_roles[drone_list[drone]] = oil_spills[oil_idx]
                    potentials[:, drone] = -999

            return drone_roles """

    def agent_decision(self) -> None:
        if self.clean_waters.tile_dict[self.point].with_oil:
            self.clean_water()

        elif self.clean_waters.tile_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            self.role = self.role_assignment()

            self.target_moving()
        return

    def needs_recharge(self) -> bool:
        return self.battery <= 150

    def target_moving(self) -> None:
        drones_around = self.see_drones_around()
        oil_points = []
        #print("id ", self.drone_id)
        #print("role ", self.role)
        if self.role is not None:

            for oil in self.role.points:
                #if oil in self.clean_waters.scanned_poi_tiles or oil in self.fov:
                 #   for tile in oil.tiles:  
                  #      if tile.sector in self.drone_sectors:           
                oil_points.append(oil)
            dir_list = give_directions(self.point, [self.point.closest_point_from_points(oil_points)])
            dirs = [d for d in dir_list if d not in give_directions(self.point, drones_around)]
            if dirs:
                self.move(random.choice(dirs))
                return
            
        # 0 -> oil/ 1-> battery
        direction_lists = poi = [[], []]
        drones_around = self.see_drones_around()
        scanned_poi = list(self.clean_waters.scanned_poi_tiles.keys())
        observed_points = scanned_poi + self.fov if scanned_poi else self.fov

        for point in observed_points:
            if self.clean_waters.tile_dict[point].__class__ == Recharger and self.needs_recharge() and self.clean_waters.tile_dict[point].sector in self.drone_sectors:
                poi[1].append(point)            
            elif self.clean_waters.tile_dict[point].with_oil and self.clean_waters.tile_dict[point].sector in self.drone_sectors:
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

        #not_poi = [d for d in all_directions if d not in give_directions(self.point, drones_around)]
        #self.move(random_direction()) #if not_poi else self.move(-1)