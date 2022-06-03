from drones.drone import Drone
import random
from utils.settings import FOV_ACTUATOR_RANGE
from environment.tile import Recharger
from utils.util import Direction, random_direction


class DroneGreedy(Drone):
    def __init__(self, clean_waters, x, y):
        super().__init__(clean_waters, x, y)
        self.fov_range = FOV_ACTUATOR_RANGE

    def agent_decision(self) -> None:
        if self.clean_waters.tile_dict[self.point].with_oil:
            self.clean_water()

        elif self.clean_waters.tile_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            self.target_moving()
        return

    def needs_recharge(self) -> bool:
        return self.battery <= 50

    def target_moving(self) -> None:
        def give_directions(ps: list) -> list:
            directions = []
            for p in ps:
                if len(directions) == 4:
                    break
                if p.x > self.point.x and Direction.West not in directions:
                    directions.append(Direction.West)
                if p.x < self.point.x and Direction.East not in directions:
                    directions.append(Direction.East)
                if p.y > self.point.y and Direction.South not in directions:
                    directions.append(Direction.South)
                if p.y < self.point.y and Direction.North not in directions:
                    directions.append(Direction.North)
            return directions

        # 0 -> oil/ 1-> battery
        points_of_interest = [[], []]
        direction_lists = [[], []]
        all_directions = [Direction.West, Direction.East, Direction.South, Direction.North]
        drones_around = self.see_drones_around()

        for point in self.fov:
            if self.clean_waters.tile_dict[point].with_oil:
                points_of_interest[0].append(point)

            elif self.clean_waters.tile_dict[point].__class__ == Recharger and self.needs_recharge():
                points_of_interest[1].append(point)

        if points_of_interest[0] or points_of_interest[1]:
            for i in range(0, 2):
                direction_lists[i] = give_directions(points_of_interest[i])

            for direction_list in direction_lists:
                dirs = [d for d in direction_list if d not in give_directions(drones_around)]  # dont collide with other
                if dirs:
                    self.move(random.choice(dirs))
                    return

        temp = [d for d in all_directions if d not in give_directions(drones_around)]

        self.move(random_direction()) if temp else self.move(-1)
