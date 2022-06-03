from typing import List

from drones.drone import Drone
from utils.settings import *
from utils.util import *
from environment.tile import Recharger


class Desire(Enum):
    Recharge = 1
    Move_to_Sector = 2
    Clean_Water = 3
    Find_Fire = 4


class Action(Enum):
    Recharge = 1
    Clean = 2
    Move_North = 3
    Move_South = 4
    Move_East = 5
    Move_West = 6


def direction_action(from_point, to_point):
    x_move = to_point.x - from_point.x
    if x_move == 1:
        return Action.Move_West
    elif x_move == -1:
        return Action.Move_East

    y_move = to_point.y - from_point.y
    if y_move == 1:
        return Action.Move_South
    elif y_move == -1:
        return Action.Move_North


class DroneHybrid(Drone):
    def __init__(self, clean_waters, x, y, tile_dict: dict):
        super().__init__(clean_waters, x, y)
        self.map = tile_dict
        self.intention = {"Desire": None, "Point": None}
        self.sectors_on_fire = clean_waters.hybrid_drone_sectors_on_fire
        self.points_on_fire = clean_waters.hybrid_drone_points_on_fire
        self.visited_sector_tiles = []
        self.plan_queue = []
        self.last_action = None

    def can_reactive_decision(self) -> bool:
        desire = self.intention.get("Desire")
        tile_class = self.map[self.point].__class__

        if desire == Desire.Recharge: return tile_class == Recharger
        if self.battery < 75 and tile_class == Recharger:
            return True
        elif self.map[self.point].with_oil:
            return True
        return False

    def simple_reactive_action(self) -> None:
        tile_class = self.map[self.point].__class__

        if self.battery < 75 and tile_class == Recharger:
            self.execute(Action.Recharge)
        elif self.map[self.point].with_oil:
            self.execute(Action.Clean)

    def agent_decision(self) -> None:
        self.update_beliefs()

        if self.can_reactive_decision():
            self.simple_reactive_action()
        elif len(self.plan_queue) > 0 and not self.intention_success():
            action = self.plan_queue.pop(0)
            if self.is_plan_sound(action):
                self.execute(action)
            else:
                self.rebuild_plan()

            if self.reconsider():
                self.deliberate()
                self.build_plan()
        else:
            self.deliberate()
            self.build_plan()

    def update_beliefs(self):
        self.fov = self.calculate_fov()
        for point in self.fov:
            if self.map[point].with_oil and point not in self.points_on_fire:
                self.points_on_fire.append(point)
                for sec in self.clean_waters.sector_list:
                    if point in sec.sectorTiles and sec not in self.sectors_on_fire:
                        self.sectors_on_fire.append(sec)

    def deliberate(self) -> None:
        desires = []

        # Generate Options
        if self.needs_recharge():
            desires.append(Desire.Recharge)
        if self.sector_on_fire():
            if self.point not in self.sectors_on_fire[0].sectorTiles:
                desires.append(Desire.Move_to_Sector)
            else:
                desires.append(Desire.Clean_Water)
        if not desires:
            desires.append(Desire.Find_Fire)

        # Filtering Options
        if Desire.Recharge in desires:
            self.intention = {"Desire": Desire.Recharge,
                              "Point": self.point.closest_point_from_tiles(
                                  [tile for tile in self.map.values() if tile.__class__ == Recharger])}
        elif Desire.Clean_Water in desires:
            self.intention = {"Desire": Desire.Clean_Water,
                              "Point": self.most_interest_point()}
        elif Desire.Move_to_Sector in desires:
            self.intention = {"Desire": Desire.Move_to_Sector,
                              "Point": self.point.closest_point_from_points(self.sectors_on_fire[0].sectorTiles)}
        else:
            point = random.choice([p for p in self.fov if p != self.point])
            self.intention = {"Desire": Desire.Find_Fire, "Point": point}

    # plan generation and rebuild
    def reconsider(self) -> bool:
        return (self.intention.get("Desire") != Desire.Recharge) and self.needs_recharge()

    def intention_success(self) -> bool:
        desire = self.intention.get("Desire")

        if desire == Desire.Recharge:
            return self.last_action == Action.Recharge
        elif desire == Desire.Clean_Water:
            return False
        elif desire == Desire.Move_to_Sector:
            return self.point == self.intention.get("Point")
        else:
            # find fire
            return [point for point in self.fov if self.map[point].with_oil] != []

    def build_plan(self):
        self.plan_queue = self.build_path_plan(self.point, self.intention.get("Point"))

        desire = self.intention.get("Desire")
        if desire == Desire.Recharge:
            self.plan_queue.append(Action.Recharge)

        print(desire)
        print(self.plan_queue)

    def build_path_plan(self, start: Point, dest: Point):
        path = print_path_point(start.find_path_bfs_from(dest, self.map))
        # print(path)

        result_plan = []
        while len(path) > 1:
            result_plan.append(direction_action(path[0], path[1]))
            path = path[1:]
        return result_plan

    def rebuild_plan(self):
        self.plan_queue = []
        self.reactive_behaviour()

    def is_plan_sound(self, action: Action) -> bool:
        if action == Action.Recharge:
            return self.clean_waters.tile_dict[self.point].__class__ == Recharger and self.can_recharge()
        elif action == Action.Move_North:
            return Point(self.point.x, self.point.y + 1) not in self.drone_positions_list()
        elif action == Action.Move_South:
            return Point(self.point.x, self.point.y - 1) not in self.drone_positions_list()
        elif action == Action.Move_East:
            return Point(self.point.x - 1, self.point.y) not in self.drone_positions_list()
        else:
            # move West
            return Point(self.point.x + 1, self.point.y) not in self.drone_positions_list()

    # plan execution
    def execute(self, action: Action) -> None:
        if action == Action.Clean:
            self.clean_water()
        elif action == Action.Recharge:
            self.recharge()
        elif action == Action.Move_North:
            self.move(Direction.North)
        elif action == Action.Move_South:
            self.move(Direction.South)
        elif action == Action.Move_East:
            self.move(Direction.East)
        else:
            self.move(Direction.West)
        self.last_action = action

    def needs_recharge(self) -> bool:
        populations = [tile for tile in self.map.values() if tile.__class__ == Recharger]
        closest_recharge_point = self.point.closest_point_from_tiles(populations)
        return (number_of_steps_from_x_to_y(self.point, closest_recharge_point) + 1) * MOVEBATTERYCOST >= self.battery

    def sector_on_fire(self) -> bool:
        return self.sectors_on_fire != []

    def can_recharge(self) -> bool:
        return self.battery < 100

    def drone_positions_list(self) -> list:
        return [drone.point for drone in self.clean_waters.drone_list]

    def get_maximized_dists_point(self, points: List[Point]) -> Point:
        # filtered by sector
        drones_in_sector = [p for p in self.drone_positions_list() if p in self.sectors_on_fire[0].sectorTiles]
        if not drones_in_sector: return points[0]

        point = points[0]
        sum_max = sum([point.distance_to(d) for d in drones_in_sector])
        for i in range(1, len(points)):
            dists = [points[i].distance_to(d) for d in drones_in_sector]
            point = (point, points[i])[sum(dists) > sum_max]
            sum_max = (sum_max, sum(dists))[sum(dists) > sum_max]
        print(point)
        return point

    def most_interest_point(self) -> Point:
        if self.point not in self.visited_sector_tiles:
            self.visited_sector_tiles.append(self.point)
        non_visited = [p for p in self.fov if p not in self.visited_sector_tiles]
        # filtered by sector and fire
        on_fire = [p for p in non_visited if self.map[p].with_oil and p in self.sectors_on_fire[0].sectorTiles]
        not_on_fire = [p for p in non_visited if p in self.sectors_on_fire[0].sectorTiles]
        interests = (not_on_fire, on_fire)[len(on_fire) > 0]

        # filtered by priority
        max_priority = self.map[interests[0]].priority
        for p in interests:
            max_priority = (max_priority, self.map[p].priority)[self.map[p].priority > max_priority]
        max_points = [p for p in interests if self.map[p].priority == max_priority]
        if len(max_points) == 1: return max_points[0]

        # filtered by max distance to other drones in sector
        return self.get_maximized_dists_point(max_points)

    def reactive_behaviour(self) -> None:
        if self.map[self.point].with_oil:
            if self.point not in self.clean_waters.hybrid_drone_points_on_fire:
                self.clean_waters.hybrid_drone_points_on_fire.append(self.point)
        elif self.map[self.point].__class__ == Recharger:
            if self.can_recharge():
                self.recharge()
            else:
                self.target_moving()
        else:
            self.target_moving()
        return
