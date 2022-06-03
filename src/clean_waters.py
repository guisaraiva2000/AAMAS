import math

from drones.greedy import DroneGreedy
from drones.random import DroneRandom
from environment.map import *
from drones.hybrid import DroneHybrid
from environment.oil import *
from environment.sector import *
from utils.button import *
import time


class CleanWaters:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, True
        self.screen = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
        self.tile_group = pygame.sprite.Group()  # use to draw and do update to tiles
        self.drone_group = pygame.sprite.Group()  # use to draw and do update to drones
        self.tile_dict = {}  # to save created tiles
        self.hybrid_drone_map = {}  # none actualized tile map for hybrid drone
        self.drone_list = []
        self.wind = Wind(
            random.choice([Direction.North, Direction.South, Direction.East, Direction.West]),
            random.randint(1, 10))
        self.wind_display = Button(PURPLE, 40, 450, 180, 30,
                                   "Wind direction: " + str(self.wind.direction).split(".")[1])
        self.oil_list: List[Oil] = []
        self.sector_list: List[Sector] = []
        self.recharger_list: List[Tile] = []

        self.hybrid_drone_sectors_on_fire: List[Sector] = []
        self.hybrid_drone_points_on_fire: List[Point] = []

        # button, step counter and variable that make sim do one step in step mode
        self.step_counter = 0

        # button and var that says to create greedy drones
        self.greedy_drone_button = None
        self.create_greedy_drone = False

        # button and var that indicates to create hybrid drones
        self.hybrid_drone_button = None
        self.create_hybrid_drone = False

        # button and var that indicates to create hybrid coop drones
        self.random_drone_button = None
        self.create_random_drone = False

        self.drone_not_chosen = True

    def main_loop(self):
        self.initial_draw()
        while self.drone_not_chosen and self.playing and self.running:
            self.check_events()
        self.init_and_draw_drones()
        time.sleep(0.5)
        while self.playing:
            self.step_counter += 1

            if self.check_end_conditions():
                print("------------Game Over------------")
                self.calculate_metrics()
                self.drone_not_chosen = True

                while self.playing and self.running:
                    self.check_events()
                break

            self.check_events()

            for agent in self.drone_list:
                agent.agent_decision()

            for oil in self.oil_list:
                update_oil(oil)
                expand_oil(oil, self.tile_dict, self.wind)
                if not oil.stop_time and not len(oil.tiles):
                    oil.stop_time = self.step_counter

            for sector in self.sector_list:
                if sector.calculate_oil_alert(self.oil_list):
                    print("Oil detected in sector " + str(sector.sectorID))
                    self.hybrid_drone_sectors_on_fire.append(sector)

                if not sector.withOil and sector in self.hybrid_drone_sectors_on_fire:
                    # remove sector from drone list
                    self.hybrid_drone_sectors_on_fire.remove(sector)

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
                    self.create_greedy_drone = False
                    self.create_hybrid_drone = False
                    self.drone_not_chosen = False
                    if not self.oil_list:
                        self.create_oil_spills()
                if self.greedy_drone_button.is_over(mouse_position):
                    self.create_greedy_drone = True
                    self.create_hybrid_drone = False
                    self.create_random_drone = False
                    self.drone_not_chosen = False
                    if not self.oil_list:
                        self.create_oil_spills()
                if self.hybrid_drone_button.is_over(mouse_position):
                    self.create_hybrid_drone = True
                    self.create_greedy_drone = False
                    self.create_random_drone = False
                    self.drone_not_chosen = False
                    if not self.oil_list:
                        self.create_oil_spills()

    # Create things

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
                self.hybrid_drone_map[tile.point] = tile

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

    def create_hybrid_drones(self):
        drone = DroneHybrid(self, 16, 16, self.hybrid_drone_map)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        """drone = DroneHybrid(self, 15, 16, self.hybrid_drone_map)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneHybrid(self, 17, 16, self.hybrid_drone_map)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneHybrid(self, 15, 17, self.hybrid_drone_map)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        drone = DroneHybrid(self, 16, 17, self.hybrid_drone_map)
        self.drone_group.add(drone)
        self.drone_list.append(drone)"""
        drone = DroneHybrid(self, 17, 17, self.hybrid_drone_map)
        self.drone_group.add(drone)
        self.drone_list.append(drone)
        """drone = DroneHybrid(self, 15, 18, self.hybrid_drone_map)
        self.drone_group.add(drone)
        self.drone_list.append(drone)"""
        drone = DroneHybrid(self, 16, 18, self.hybrid_drone_map)
        self.drone_group.add(drone)
        self.drone_list.append(drone)

    def create_sectors(self):
        sector_id = 1
        sector_size = 8
        for y in range(0, 32 // sector_size, 1):
            for x in range(0, 32 // sector_size, 1):
                # id, probability per oil, size
                sector = Sector(sector_id, 16 / 64, sector_size)
                sector_id += 1
                sector.create_sector(x * sector_size, y * sector_size)
                self.sector_list.append(sector)

    def create_oil_spills(self):
        rng = random.randint(1, 3)
        print(f"Oil count: {rng}")
        for i in range(1, rng + 1):
            lst = [x for x in self.tile_dict.values() if x.__class__ == Ocean]
            point = random.choice(lst).point
            oil_spill = self.tile_dict[point]
            oil = Oil(i, point, 1)
            oil_spill.with_oil = True
            oil.add_oil(oil_spill)
            self.oil_list.append(oil)

    def create_buttons(self):
        self.random_drone_button = Button(WHITE, 40, 29, 180, 30, 'Random Drones')
        self.greedy_drone_button = Button(WHITE, 40, 79, 180, 30, 'Greedy Drones')
        self.hybrid_drone_button = Button(WHITE, 600, 40, 160, 30, 'Start with hybrid drones')

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
        self.random_drone_button.draw(self.screen)
        self.wind_display.draw(self.screen)
        # self.hybrid_drone_button.draw(self.screen)

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

        if self.create_hybrid_drone:
            self.create_hybrid_drones()

        if self.create_random_drone:
            self.create_random_drones()

        self.draw_drones()
        pygame.display.flip()

    def check_end_conditions(self):
        if len(self.drone_list) == 0:
            print("All Drones Died")
            return True

        n_tiles_w_oil = 0
        for oil in self.oil_list:
            n_tiles_w_oil += len(oil.tiles)

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
