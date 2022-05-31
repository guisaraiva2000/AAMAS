import pygame
from utils.settings import *
import math
from abc import ABC, abstractmethod
from utils.util import Point
from utils.util import Direction


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
        self.fov_range = FOV_DEFAULT_RANGE
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

        for i in range(y - self.fov_range, y + self.fov_range + 1):
            for j in range(x - self.fov_range + 1, x + self.fov_range + 1):
                if not (i < 0 or i > 31 or j < 0 or j > 31):
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

    def see_drones_around(self) -> list:
        return [drone.point for drone in self.simulation.drone_list
                if math.dist([self.point.x, self.point.y], [drone.point.x, drone.point.y]) == 1]

    @abstractmethod
    def agent_decision(self):
        pass

    @abstractmethod
    def needs_recharge(self):
        pass

    @abstractmethod
    def target_moving(self) -> None:
        pass
