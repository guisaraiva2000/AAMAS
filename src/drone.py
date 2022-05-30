import pygame
from settings import *
import math
import random
from abc import ABC, abstractmethod
from util import Point, random_direction
from tile import Recharger
from util import Direction


class Drone(pygame.sprite.Sprite, ABC):
    def __init__(self, simulation, x, y):
        super().__init__()
        self.simulation = simulation
        self.image = pygame.Surface((DRONESIZE, DRONESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.point = Point(x, y)
        self.rect.center = \
            [int((self.point.x * TILESIZE) + TILE_MARGIN_X), int((self.point.y * TILESIZE) + TILE_MARGIN_Y)]
        self.battery = BATTERY
        self.fov = self.calculate_fov()

    def recharge(self) -> None:
        self.battery = BATTERY
        return

    def spend_energy(self) -> None:
        self.battery -= MOVEBATTERYCOST

    def move(self, direction) -> None:
        if direction == -1:
            self.spend_energy()
            self.is_dead()
            self.fov = self.calculate_fov()
            return

        drone_points = []
        for drone in self.simulation.drone_list:
            drone_points.append(drone.point)

        point = self.point
        if direction == Direction.West:
            if self.point.x < 31:
                point = Point(self.point.x + 1, self.point.y)
        elif direction == Direction.East:
            if self.point.x > 0:
                point = Point(self.point.x - 1, self.point.y)
        elif direction == Direction.South:
            if self.point.y < 31:
                point = Point(self.point.x, self.point.y + 1)
        else:
            if self.point.y > 0:
                point = Point(self.point.x, self.point.y - 1)

        if point not in drone_points:
            self.point = point
            self.rect.center = [int((self.point.x * TILESIZE) + TILE_MARGIN_X),
                                int((self.point.y * TILESIZE) + TILE_MARGIN_Y)]

        self.spend_energy()
        self.is_dead()
        self.fov = self.calculate_fov()
        return

    def calculate_fov(self) -> list:
        fov = []
        x = self.point.x
        y = self.point.y

        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if i < 0 or i > 31 or j < 0 or j > 31:
                    continue
                fov.append(Point(j, i))
        return fov

    def clean_water(self) -> None:
        tile = self.simulation.tile_dict[self.point]
        tile.with_oil = False

        self.spend_energy()
        self.is_dead()
        return

    def is_dead(self):
        if self.battery <= 0:
            self.simulation.drone_list.remove(self)
            self.kill()

    def target_moving(self) -> None:
        def give_directions(ps: list) -> list:
            directions = []
            for p in ps:
                if len(directions) == 4:
                    break
                if p.x > self.point.x:
                    if Direction.West not in directions:
                        directions.append(Direction.West)
                if p.x < self.point.x:
                    if Direction.East not in directions:
                        directions.append(Direction.East)
                if p.y > self.point.y:
                    if Direction.South not in directions:
                        directions.append(Direction.South)
                if p.y < self.point.y:
                    if Direction.North not in directions:
                        directions.append(Direction.North)
            return directions

        # 0 -> oil/ 1-> battery
        points_of_interest = [[], []]
        direction_lists = [[], []]
        all_directions = [Direction.West, Direction.East, Direction.South, Direction.North]
        drones_around = self.see_drones_around()

        for point in self.fov:
            if self.simulation.tile_dict[point].with_oil:
                points_of_interest[0].append(point)
                continue
            if self.simulation.tile_dict[point].__class__ == Recharger and self.needs_recharge():
                points_of_interest[1].append(point)
                continue

        if points_of_interest[0] or points_of_interest[1]:
            for i in range(0, 2):
                direction_lists[i] = give_directions(points_of_interest[i])

            for direction_list in direction_lists:
                dirs = [d for d in direction_list if d not in give_directions(drones_around)]
                if dirs:
                    self.move(random.choice(dirs))
                    return

        temp = [d for d in all_directions if d not in give_directions(drones_around)]
        if temp:
            self.move(random_direction())
            return
        else:
            self.move(-1)
            return

    def see_drones_around(self) -> list:
        return [drone.point for drone in self.simulation.drone_list
                if math.dist([self.point.x, self.point.y], [drone.point.x, drone.point.y]) == 1]

    @abstractmethod
    def agent_decision(self):
        pass

    @abstractmethod
    def needs_recharge(self):
        pass


class DroneNaive(Drone):
    def __init__(self, simulation, x, y):
        super().__init__(simulation, x, y)

    def agent_decision(self):
        if self.simulation.tile_dict[self.point].with_oil:
            self.clean_water()

        elif self.simulation.tile_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            self.move(random_direction())

    def needs_recharge(self):
        return self.battery < 90


class DroneReactive(Drone):
    def __init__(self, simulation, x, y):
        super().__init__(simulation, x, y)

    def agent_decision(self) -> None:
        if self.simulation.tile_dict[self.point].with_oil:
            self.clean_water()

        elif self.simulation.tile_dict[self.point].__class__ == Recharger and self.needs_recharge():
            self.recharge()

        else:
            self.target_moving()
        return

    def needs_recharge(self) -> bool:
        return self.battery <= 50
