import pygame
import math
import random
from environment.square import Recharger
from utils.settings import *
from abc import ABC, abstractmethod
from utils.util import Point, get_directions, random_direction, all_directions
from utils.util import Direction


class Drone(pygame.sprite.Sprite, ABC):
    def __init__(self, clean_waters, x, y, color):
        super().__init__()
        self.clean_waters = clean_waters
        self.image = pygame.Surface((DRONE_SIZE, DRONE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.point = Point(x, y)
        self.rect.center = \
            [int((self.point.x * SQUARE_SIZE) + SQUARE_MARGIN_X), int((self.point.y * SQUARE_SIZE) + SQUARE_MARGIN_Y)]
        self.battery = BATTERY
        self.fov_range = FOV_DEFAULT_RANGE
        self.fov = self.calculate_fov()

    def recharge(self) -> None:
        self.battery = BATTERY
        return

    def spend_energy(self) -> None:
        self.battery -= MOVE_BATTERY_COST

    def move(self, direction, bounds=(0, 31, 0, 31)) -> None:
        if direction == -1:
            self.spend_energy()
            self.is_dead()
            self.fov = self.calculate_fov()
            return

        drone_points = []
        for drone in self.clean_waters.drone_list:
            drone_points.append(drone.point)

        point = self.point
        if direction == Direction.West and self.point.x > bounds[0]:
            point = Point(self.point.x - 1, self.point.y)
        elif direction == Direction.East and self.point.x < bounds[1]:
            point = Point(self.point.x + 1, self.point.y)
        elif direction == Direction.South and self.point.y < bounds[3]:
            point = Point(self.point.x, self.point.y + 1)
        elif self.point.y > bounds[2]:
            point = Point(self.point.x, self.point.y - 1)

        if point not in drone_points:
            self.point = point
            self.rect.center = [int((self.point.x * SQUARE_SIZE) + SQUARE_MARGIN_X),
                                int((self.point.y * SQUARE_SIZE) + SQUARE_MARGIN_Y)]

        self.spend_energy()
        self.is_dead()
        self.fov = self.calculate_fov()
        return

    def calculate_fov(self) -> list:
        fov = []
        x, y = self.point.x, self.point.y

        for i in range(y - self.fov_range, y + self.fov_range + 1):
            for j in range(x - self.fov_range + 1, x + self.fov_range + 1):
                if not (i < 0 or i > 31 or j < 0 or j > 31 or i == y or j == x):
                    fov.append(Point(j, i))

        return fov

    def clean_water(self) -> None:
        self.clean_waters.total_cleaned_squares += 1

        self.clean_waters.square_dict[self.point].with_oil = False
        self.clean_waters.scanned_poi_squares.pop(self.point, None)

        self.spend_energy()
        self.is_dead()
        return

    def is_dead(self):
        if self.battery <= 0:
            self.clean_waters.drone_list.remove(self)
            self.kill()

    def see_drones_around(self) -> list:
        return [drone.point for drone in self.clean_waters.drone_list if self.point.distance_to(drone.point) == 1]

    def movement(self, bounds=(0, 31, 0, 31), zones=(0, 1, 2, 3, 4, 5, 6, 7), role=None):
        # 0 -> battery/ 1-> oil
        direction_lists = poi = [[], []]
        scanned_poi = list(self.clean_waters.scanned_poi_squares.keys())
        observed_points = scanned_poi + self.fov if scanned_poi else self.fov

        for point in observed_points:
            if self.clean_waters.square_dict[point].__class__ == Recharger and self.needs_recharge() and \
                    self.clean_waters.square_dict[point].zone in zones:
                poi[0].append(point)

            elif self.clean_waters.square_dict[point].with_oil and self.clean_waters.square_dict[point].zone in zones:
                if role is not None:
                    if point in role.points:
                        poi[1].append(point)
                else:
                    poi[1].append(point)

        if poi[0]:
            direction_lists[0] = get_directions(self.point, [self.point.closest_point_from_points(poi[0])])
        if poi[1]:
            direction_lists[1] = get_directions(self.point, [self.point.closest_point_from_points(poi[1])])

        for direction_list in direction_lists:
            dirs = [d for d in direction_list if d not in get_directions(self.point, self.see_drones_around())]
            if dirs:
                self.move(random.choice(dirs), bounds)
                return

        not_poi = [d for d in all_directions if d not in get_directions(self.point, self.see_drones_around())]
        self.move(random_direction(), bounds) if not_poi else self.move(-1)

    @abstractmethod
    def agent_decision(self):
        pass

    @abstractmethod
    def needs_recharge(self):
        pass

