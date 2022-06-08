import math
import random

from drones.greedy import DroneGreedy
from drones.greedy_w_roles import DroneGreedyRoles
from drones.random import DroneRandom
from drones.scanner import DroneScanner
from environment.map import *
from environment.oil import *
from environment.sector import *
from utils.button import *
import time

from utils.util import all_directions


class CleanWaters:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, True
        self.screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
        self.tile_group = pygame.sprite.Group()  # use to draw and do update to tiles
        self.drone_group = pygame.sprite.Group()  # use to draw and do update to drones
        self.tile_dict = {}  # to save created tiles
        self.scanned_poi_tiles = {}
        self.drone_list = []
        self.wind = Wind(random.choice(all_directions), 5)  # random.randint(1, 10))
        self.wind_display = Button(PURPLE, 40, 450, 180, 30,
                                   "Wind direction: " + str(self.wind.direction).split(".")[1])
        self.oil_list: List[Oil] = []
        self.sector_list: List[Sector] = []
        self.recharger_list: List[Tile] = []

        self.step_counter = 0

        # button and var that says to create greedy drones
        self.greedy_drone_button = None
        self.create_greedy_drone = False

        # button and var that says to create greedy drones
        self.greedy_w_roles_drone_button = None
        self.create_greedy_w_roles_drone = False

        # button and var that indicates to create random drones
        self.random_drone_button = None
        self.create_random_drone = False

        # var that says to create scanner drones
        self.create_scanner_drone = False

        self.drone_not_chosen = True

    def main_loop(self):
        self.initial_draw()
        while self.drone_not_chosen and self.playing and self.running:
            self.check_events()
        self.init_and_draw_drones()

        time.sleep(0.5)
        can_expand_oil = True

        while self.playing:
            self.step_counter += 1

            if self.check_end_conditions():
                print("------------Game Over------------")
                self.calculate_metrics()
                self.drone_not_chosen = True

                while self.playing and self.running:
                    self.check_events()
                break

            for agent in self.drone_list:
                agent.agent_decision()

            active_oil_spill_counter = len(self.oil_list)
            for oil in self.oil_list:
                update_oil(oil)

                if can_expand_oil:
                    expand_oil(oil, self.tile_dict, self.wind)

                if not len(oil.tiles):
                    active_oil_spill_counter -= 1
                    if not oil.stop_time:
                        oil.stop_time = self.step_counter

            if active_oil_spill_counter < random.randint(2, 3):
                self.create_oil_spills()

            can_expand_oil = not can_expand_oil  # expand every two steps only
            self.update()
            self.draw()
            time.sleep(0.1)

        while self.drone_not_chosen and self.playing and self.running:
            self.check_events()

    def check_events(self):
        for event in pygame.event.get():
            mouse_position = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.random_drone_button.is_over(mouse_position):
                    self.create_random_drone = True
                    self.create_scanner_drone = False
                    self.create_greedy_drone = False
                    self.drone_not_chosen = False
                    if not self.oil_list:
                        self.create_oil_spills()
                if self.greedy_drone_button.is_over(mouse_position):
                    self.create_greedy_drone = True
                    self.create_scanner_drone = True
                    self.create_random_drone = False
                    self.drone_not_chosen = False
                    if not self.oil_list:
                        self.create_oil_spills()
                if self.greedy_w_roles_drone_button.is_over(mouse_position):
                    self.create_greedy_w_roles_drone = True
                    self.create_scanner_drone = True
                    self.create_greedy_drone = False
                    self.create_random_drone = False
                    self.drone_not_chosen = False
                    if not self.oil_list:
                        self.create_oil_spills()

    def create_tiles(self):
        for y in range(0, 32, 1):
            for x in range(0, 32, 1):
                if sim_map[y][x][0] == "recharger":
                    tile = Recharger(self, x, y)
                    self.recharger_list.append(tile)
                else:
                    tile = Ocean(self, x, y)
                self.tile_group.add(tile)
                self.tile_dict[tile.point] = tile

    def create_random_drones(self):
        drone = DroneRandom(self, 6, 6)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneRandom(self, 10, 10)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneRandom(self, 14, 14)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneRandom(self, 18, 18)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneRandom(self, 22, 22)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneRandom(self, 26, 26)
        self.drone_group.add(drone)
        self.drone_list.append(drone)

    def create_greedy_drones(self):
        drone = DroneGreedy(self, 6, 6)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedy(self, 10, 10)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedy(self, 14, 14)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedy(self, 18, 18)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedy(self, 22, 22)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedy(self, 26, 26)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        """drone = DroneGreedy(self, 15, 18)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedy(self, 16, 18)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedy(self, 17, 18)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedy(self, 18, 18)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedy(self, 16, 19)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedy(self, 17, 19)
        self.drone_group.add(drone)
        self.drone_list.append(drone)"""

    def create_greedy_w_roles_drones(self):
        drone = DroneGreedyRoles(self, 6, 6, 0)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedyRoles(self, 10, 10, 1)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedyRoles(self, 14, 14, 2)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedyRoles(self, 18, 18, 3)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedyRoles(self, 22, 22, 4)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneGreedyRoles(self, 26, 26, 5)
        self.drone_group.add(drone)
        self.drone_list.append(drone)

    def create_scanner_drones(self):
        drone = DroneScanner(self, 8, 24)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneScanner(self, 16, 16)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneScanner(self, 22, 10)
        self.drone_group.add(drone)
        self.drone_list.append(drone)

    def create_sectors(self):
        sector_id = 0
        sector_size = 8
        for y in range(0, 32 // sector_size, 1):
            for x in range(0, 32 // sector_size, 1):
                sector = Sector(self, sector_id, sector_size)
                sector_id += 1
                sector.create_sector(x * sector_size, y * sector_size)
                self.sector_list.append(sector)

    def create_oil_spills(self):
        lst = [x for x in self.tile_dict.values() if x.__class__ == Ocean]
        point = random.choice(lst).point
        oil_spill = self.tile_dict[point]
        oil = Oil(len(self.oil_list), point, 1)
        oil_spill.with_oil = True
        oil.add_oil(oil_spill)
        self.oil_list.append(oil)

    def create_buttons(self):
        self.random_drone_button = Button(WHITE, 40, 29, 180, 30, 'Random Drones')
        self.greedy_drone_button = Button(WHITE, 40, 79, 180, 30, 'Greedy Drones')
        self.greedy_w_roles_drone_button = Button(WHITE, 40, 129, 180, 30, 'Role Drones')

    def draw(self):
        self.update_tiles()
        self.draw_tiles()
        self.draw_grid()
        self.draw_drones()
        self.draw_buttons()
        pygame.display.flip()

    def initial_draw(self):
        self.update_tiles()
        self.draw_tiles()
        self.draw_grid()
        self.draw_buttons()
        pygame.display.flip()

    def draw_grid(self):
        for x in range(0, GRID_W + 1, TILESIZE):
            if x % 128 == 0:
                pygame.draw.line(self.screen, PURPLE, (x + GRID_MARGIN_X, GRID_MARGIN_Y),
                                 (x + GRID_MARGIN_X, GRID_H + GRID_MARGIN_Y))
            else:
                pygame.draw.line(self.screen, WHITE, (x + GRID_MARGIN_X, GRID_MARGIN_Y),
                                 (x + GRID_MARGIN_X, GRID_H + GRID_MARGIN_Y))
        for y in range(0, GRID_H + 1, TILESIZE):
            if y % 128 == 0:
                pygame.draw.line(self.screen, PURPLE, (GRID_MARGIN_X, y + GRID_MARGIN_Y),
                                 (GRID_W + GRID_MARGIN_X, y + GRID_MARGIN_Y))
            else:
                pygame.draw.line(self.screen, WHITE, (GRID_MARGIN_X, y + GRID_MARGIN_Y),
                                 (GRID_W + GRID_MARGIN_X, y + GRID_MARGIN_Y))

    def draw_tiles(self):
        self.tile_group.draw(self.screen)

    def draw_drones(self):
        self.drone_group.draw(self.screen)

    def draw_buttons(self):
        self.greedy_drone_button.draw(self.screen)
        self.greedy_w_roles_drone_button.draw(self.screen)
        self.random_drone_button.draw(self.screen)
        self.wind_display.draw(self.screen)

    def update(self):
        self.tile_group.update()
        self.drone_group.update()

    def update_tiles(self):
        for tile in self.tile_dict.values():
            if tile.__class__ == Recharger:
                color = RED
            elif tile.with_oil:
                color = BLACK
            else:
                color = BLUE

            tile.image.fill(color)

    def initiate(self):
        self.create_buttons()
        self.create_tiles()
        self.create_sectors()

    def init_and_draw_drones(self):
        if self.create_greedy_drone:
            self.create_greedy_drones()

        if self.create_greedy_w_roles_drone:
            self.create_greedy_w_roles_drones()

        if self.create_random_drone:
            self.create_random_drones()

        if self.create_scanner_drone:
            self.create_scanner_drones()

        self.draw_drones()
        pygame.display.flip()

    def check_end_conditions(self):
        if len(self.drone_list) == 0:
            print("All Drones Died")
            return True

        n_tiles_w_oil = sum([len(oil.tiles) for oil in self.oil_list])
        if n_tiles_w_oil >= math.pow(GRID_W / TILESIZE, 2) / 2:
            print("Oil Covered Half Ocean")
            return True

        return False

    def calculate_metrics(self):
        print("Total Steps:", self.step_counter)
        print("Number of Oil Spills:", len(self.oil_list))
        for oil in self.oil_list:
            print("--------------------------------------\n{}".format(oil))
            if oil.stop_time:
                print("Time to clean:", oil.stop_time - oil.start_time)
            else:
                print("Time to clean: Was not cleaned.")
