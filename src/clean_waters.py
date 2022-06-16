import math
import random

from drones.greedy import DroneGreedy
from drones.greedy_w_roles import DroneGreedyRoles
from drones.random import DroneRandom
from drones.social_convention import DroneSocialConvention
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
        self.wind = Wind(random.choice(all_directions),  random.randint(MIN_WIND, MAX_WIND))
        self.wind_display = None
        self.oil_list: List[Oil] = []

        self.step_counter = 0

        # button and var that says to create greedy drones
        self.greedy_drone_button = None
        self.create_greedy_drone = False

        # button and var that says to create greedy drones
        self.greedy_w_roles_drone_button = None
        self.create_greedy_w_roles_drone = False

        # button and var that says to create greedy drones
        self.social_convention_drone_button = None
        self.create_social_convention_drone = False

        # button and var that indicates to create random drones
        self.random_drone_button = None
        self.create_random_drone = False

        # var that says to create scanner drones
        self.create_scanner_drone = False

        self.drone_not_chosen = True

        # metrics
        self.metrics_button = []
        self.avg_oil_active_time = 0
        self.total_tiles_w_ocean = 0
        self.tiles_w_ocean = 0
        self.avg_tiles_w_ocean = 0
        self.total_cleaned_tiles = 0
        self.oil_left = 0
        self.total_oil_spill = 0

    def drone_chosen(self, drone_type):
        if drone_type == "Random":
            self.create_random_drone = True
        elif drone_type == "Greedy":
            self.create_greedy_drone = True
            self.create_scanner_drone = True
        elif drone_type == "Greedy w/ S. Convention":
            self.create_social_convention_drone = True
            self.create_scanner_drone = True
        elif drone_type == "Greedy w/ Roles":
            self.create_greedy_w_roles_drone = True
            self.create_scanner_drone = True
        else:
            exit(-1)
        self.drone_not_chosen = False

    def main_loop(self):
        self.initial_draw()
        while self.drone_not_chosen and self.playing and self.running:
            self.check_events()
        self.init_and_draw_drones()

        time.sleep(0.2)
        while self.playing:
            self.step_counter += 1
            for tile in self.tile_dict.values():
                if not tile.with_oil:
                    self.tiles_w_ocean += 1
            self.total_tiles_w_ocean += self.tiles_w_ocean

            if self.check_end_conditions():
                print("------------Game Over------------")
                self.calculate_metrics()
                self.draw_metrics()
                pygame.display.flip()
                break

            for agent in self.drone_list:
                agent.agent_decision()

            active_oil_spill_counter = len(self.oil_list)
            for oil in self.oil_list:
                oil.update_oil()
                oil.expand_oil(self.tile_dict, self.wind)
                if not len(oil.tiles):
                    active_oil_spill_counter -= 1
                    if not oil.stop_time:
                        oil.stop_time = self.step_counter

            if active_oil_spill_counter < 3:
                self.create_oil_spills()

            self.update()
            self.draw()
            self.tiles_w_ocean = 0
            #time.sleep(0.05)

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
                if self.social_convention_drone_button.is_over(mouse_position):
                    self.create_social_convention_drone = True
                    self.create_scanner_drone = True
                    self.create_greedy_drone = False
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

    def create_social_convention_drones(self):
        drone = DroneSocialConvention(self, 8, 8, 0)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneSocialConvention(self, 24, 8, 1)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneSocialConvention(self, 8, 24, 2)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneSocialConvention(self, 24, 24, 3)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneSocialConvention(self, 8, 16, 4)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneSocialConvention(self, 24, 16, 5)
        self.drone_group.add(drone)
        self.drone_list.append(drone)

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
        drone = DroneScanner(self, 7, 7, 0)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneScanner(self, 23, 7, 1)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneScanner(self, 7, 23, 2)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneScanner(self, 23, 23, 3)
        self.drone_group.add(drone)
        self.drone_list.append(drone)

    def create_sectors(self):
        sector_id = 0
        sector_height = 8
        sector_width = 16
        for y in range(0, 32 // sector_height, 1):
            for x in range(0, 32 // sector_width, 1):
                sector = Sector(self, sector_id, sector_height, sector_width)
                sector_id += 1
                sector.create_sector(x * sector_width, y * sector_height)

    def create_oil_spills(self):
        lst = [x for x in self.tile_dict.values() if x.__class__ == Ocean]
        point = random.choice(lst).point
        oil_spill = self.tile_dict[point]
        oil = Oil(len(self.oil_list), point, self.step_counter)
        oil_spill.with_oil = True
        oil.add_oil(oil_spill)
        self.oil_list.append(oil)

    def create_buttons(self):
        self.wind_display = Button(DARK_BLUE, 25, 600, 200, 30,
                                   "Wind direction: " + str(self.wind.direction).split(".")[1], WHITE)
        self.random_drone_button = Button(WHITE, 25, 140, 200, 30, 'Random Drones', GREEN)
        self.greedy_drone_button = Button(WHITE, 25, 190, 200, 30, 'Greedy Drones', GREEN)
        self.social_convention_drone_button = Button(WHITE, 25, 240, 200, 30, 'Social Convention Drones', GREEN)
        self.greedy_w_roles_drone_button = Button(WHITE, 25, 290, 200, 30, 'Role Drones', GREEN)
        self.metrics_button = [Button(GREEN, 25, 390, 200, 135), Button(WHITE, 25, 390, 200, 135)]

    def draw(self):
        self.update_tiles()
        self.draw_tiles()
        self.draw_drones()
        self.draw_buttons()
        self.draw_zones()
        #self.draw_metrics()
        pygame.display.flip()

    def initial_draw(self):
        self.screen.fill(GREEN)
        self.draw_title()
        self.update_tiles()
        self.draw_tiles()
        self.draw_buttons()
        self.draw_zones()
        pygame.display.flip()

    def draw_title(self):
        font = pygame.font.SysFont('candara', 70)
        text = font.render("Clean Waters", True, WHITE)
        self.screen.blit(text, (215, 35))

    def draw_tiles(self):
        self.tile_group.draw(self.screen)

    def draw_drones(self):
        self.drone_group.draw(self.screen)

    def draw_buttons(self):
        self.greedy_drone_button.draw(self.screen)
        self.greedy_w_roles_drone_button.draw(self.screen)
        self.social_convention_drone_button.draw(self.screen)
        self.random_drone_button.draw(self.screen)
        self.wind_display.draw(self.screen)

    def draw_metrics(self):
        self.metrics_button[0].draw(self.screen, 0, 0)
        self.metrics_button[1].draw(self.screen, 2, 0)

        font = pygame.font.SysFont('candara', 15, True)
        text = font.render(f"Squares with Ocean:  {self.tiles_w_ocean}", True, WHITE)
        self.screen.blit(text, (35, 400))
        text = font.render(f"Cleaned Squares:  {self.total_cleaned_tiles}", True, WHITE)
        self.screen.blit(text, (35, 425))
        text = font.render(f"Oil Spills:  {len(self.oil_list)}", True, WHITE)
        self.screen.blit(text, (35, 450))
        text = font.render(f"Alive Drones:  {len(self.drone_list)}", True, WHITE)
        self.screen.blit(text, (35, 475))
        text = font.render(f"Steps:  {self.step_counter}", True, WHITE)
        self.screen.blit(text, (35, 500))

    def draw_zones(self):
        for x in range(0, GRID_DIM + 1, TILESIZE):
            if x % 256 == 0:
                pygame.draw.line(self.screen, RED_WINE, (x + GRID_LIMIT_X, GRID_LIMIT_Y),
                                 (x + GRID_LIMIT_X, GRID_DIM + GRID_LIMIT_Y))

        for y in range(0, GRID_DIM + 1, TILESIZE):
            if y % 128 == 0:
                pygame.draw.line(self.screen, RED_WINE, (GRID_LIMIT_X, y + GRID_LIMIT_Y),
                                 (GRID_DIM + GRID_LIMIT_X, y + GRID_LIMIT_Y))

    def update(self):
        self.tile_group.update()
        self.drone_group.update()

    def update_tiles(self):
        for tile in self.tile_dict.values():
            if tile.__class__ == Recharger:
                color = RED_WINE
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
        if self.create_scanner_drone:
            self.create_scanner_drones()

        if self.create_greedy_drone:
            self.greedy_drone_button.color = RED_WINE
            self.greedy_drone_button.text_color = WHITE
            self.create_greedy_drones()

        if self.create_social_convention_drone:
            self.social_convention_drone_button.color = RED_WINE
            self.social_convention_drone_button.text_color = WHITE
            self.create_social_convention_drones()

        if self.create_greedy_w_roles_drone:
            self.greedy_w_roles_drone_button.color = RED_WINE
            self.greedy_w_roles_drone_button.text_color = WHITE
            self.create_greedy_w_roles_drones()

        if self.create_random_drone:
            self.random_drone_button.color = RED_WINE
            self.random_drone_button.text_color = WHITE
            self.create_random_drones()

        self.draw_drones()
        pygame.display.flip()

    def check_end_conditions(self):
        #if self.step_counter == MAX_STEPS:
        #    return True

        if len(self.drone_list[4:]) == 0:
            print("All Drones Died")
            return True

        n_tiles_w_oil = sum([len(oil.tiles) for oil in self.oil_list])
        if n_tiles_w_oil >= math.pow(GRID_DIM / TILESIZE, 2) / 2:
            print("Oil Covered Half Ocean")
            return True

        return False

    def calculate_metrics(self):
        print("Total Steps:", self.step_counter)
        print("Number of Oil Spills:", len(self.oil_list))
        total_oil_active_time = 0
        for oil in self.oil_list:
            print("--------------------------------------\n{}".format(oil))
            if oil.stop_time:
                total_oil_active_time += oil.stop_time - oil.start_time
                print("Time to clean:", oil.stop_time - oil.start_time)
            else:
                total_oil_active_time += self.step_counter - oil.start_time
                self.oil_left += len(oil.tiles)
                print("Time to clean: Was not cleaned.")

        self.avg_oil_active_time = total_oil_active_time / len(self.oil_list)
        self.avg_tiles_w_ocean = self.total_tiles_w_ocean / MAX_STEPS
        self.total_oil_spill = len(self.oil_list)
