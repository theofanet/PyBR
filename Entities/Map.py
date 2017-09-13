from PyGnin import *
from opensimplex import OpenSimplex
import pygame
import random


class Map(object):
    def __init__(self, width=0, height=0, seed=0, frequency=1.0, water_lvl=0.1):
        super().__init__()
        self.width = width
        self.height = height
        self.tiles = None
        self._tileSet = Render.TileSet("assets/tileset.png")
        self._surfaces = {
            "water": (0, 0),
            "dirt": (2, 0),
            "rock": (2, 0),
            "grass": (1, 0)
        }

        # Rocks ###############################
        self._rock_tileset = Render.TileSet("assets/rocks_rotated.png", (256, 256))
        self._rock_tileset.set_scale(0.6)
        self._tile_range = (0, 7)
        self._range_between_rocks = (1, 3000)
        self._max_nb_rocks = 40
        self._rocks = [{"tile": [0, 0], "pos": [0, 0]} for x in range(self._max_nb_rocks)]
        # #####################################

        self.generate(seed, frequency, water_lvl)
        self._size = (width * 16, height * 16)
        self._mini_map = pygame.Surface((16 * width, 16 * height))
        self.draw(camera=None, surface=self._mini_map)
        self._mini_map = pygame.transform.scale(self._mini_map, (
            App.get_screen_size()[0] - 40,
            App.get_screen_size()[1] - 40
        ))

    def get_size(self):
        return self._size

    def get_surface(self, e, water=0.1):
        if e < water:
            return self._surfaces["water"]
        elif e < water + 0.2:
            return self._surfaces["grass"]
        elif e < water + 0.3:
            return self._surfaces["dirt"]
        else:
            return self._surfaces["rock"]

    @staticmethod
    def noise(nx, ny, generator):
        return generator.noise2d(nx, ny) / 2.0 + 0.5

    def generate(self, seed=0, frequency=1.0, water_lvl=0.1):
        generator = OpenSimplex(seed=seed)

        self.tiles = [[0 for x in range(self.width)] for y in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                nx = x / self.width - 0.5
                ny = y / self.height - 0.5
                e = generator.noise2d(frequency * nx, frequency * ny) / 2.0 + 0.5
                self.tiles[y][x] = self.get_surface(e, water_lvl)

        # Rocks ###############################
        used_pos = []
        for rock in self._rocks:

            keep_going = True
            pos_x = 0
            pos_y = 0

            tile_x = random.randint(self._tile_range[0], self._tile_range[1])
            tile_y = random.randint(self._tile_range[0], self._tile_range[1])

            # rocks positions generation
            while keep_going:

                # X
                if pos_x == 0:
                    pos_x = random.randint(0, 3200)  # voir pour le self.get_size
                    print("pos_x: " + repr(pos_x))

                    if used_pos:
                        for pos in used_pos:
                            diff_x = abs(pos_x-pos[0])
                            # LOG ###########################################################################
                            print("pos_x: " + repr(pos_x) + " used: " + repr(pos[0]) + " diff: " + repr(diff_x))
                            # ###############################################################################
                            if diff_x not in range(self._range_between_rocks[0], self._range_between_rocks[1]):
                                # LOG #########################################################
                                print("bad_range_x = " + repr(diff_x)
                                      + " !(" + repr(self._range_between_rocks[0])
                                      + " <> " + repr(self._range_between_rocks[1]) + ")")
                                # #############################################################
                                pos_x = 0
                                break

                # Y
                if pos_y == 0:
                    pos_y = random.randint(0, 3200) # voir pour le self.get_size
                    print("pos_y: " + repr(pos_y))

                    if used_pos:
                        for pos in used_pos:
                            diff_y = abs(pos_y-pos[1])
                            # LOG ###########################################################################
                            print("pos_y: " + repr(pos_y) + " || used: " + repr(pos[1]) + " diff: " + repr(diff_y))
                            # ###############################################################################
                            if diff_y not in range(self._range_between_rocks[0], self._range_between_rocks[1]):
                                # LOG #########################################################
                                print("bad_range_y = " + repr(diff_y)
                                      + " !(" + repr(self._range_between_rocks[0])
                                      + " <> " + repr(self._range_between_rocks[1]) + ")")
                                # #############################################################
                                pos_y = 0
                                break

                # NEXT
                if pos_x != 0 and pos_y != 0:
                    used_pos.append((pos_x, pos_y))
                    # LOG #########
                    print(used_pos)
                    # #############
                    keep_going = False

            rock["tile"][0] = tile_x
            rock["tile"][1] = tile_y
            rock["pos"][0] = pos_x
            rock["pos"][1] = pos_y

        # LOG ############
        print(self._rocks)
        # print(used_pos)
        # ################

    def draw(self, camera=None, surface=None, mini_map=False, player_position=(0, 0)):
        if not self.tiles:
            return None
        if not surface:
            surface = App.get_display()

        if mini_map:
            surface.fill((0, 0, 0))
            rect = self._mini_map.get_rect()
            rect.x += 20
            rect.y += 20
            surface.blit(self._mini_map, rect)
            x = (player_position[0] / (self._size[0])) * rect.width
            y = (player_position[1] / (self._size[1])) * rect.height
            pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(20 + x, 20 + y, 8, 10))
        else:
            x_start = 0
            x_end = self.width
            y_start = 0
            y_end = self.height

            if camera:
                x_start = int(camera.position[0] / 16) - 1
                y_start = int(camera.position[1] / 16) - 1
                x_end = x_start + int(camera.viewSize[0] / 16) + 2
                y_end = y_start + int(camera.viewSize[1] / 16) + 2

            for y in range(y_start, y_end):
                if 0 <= y < len(self.tiles):
                    for x in range(x_start, x_end):
                        if 0 <= x < len(self.tiles[y]):
                            rect = pygame.Rect(16 * x, 16 * y, 16, 16)
                            if camera:
                                rect.x -= camera.get_position()[0]
                                rect.y -= camera.get_position()[1]
                            col, row = self.tiles[y][x]
                            self._tileSet.draw_tile(col, row, rect.x, rect.y, screen=surface)

            # Rocks ###############################
            for rock in self._rocks:

                tile_x = rock["tile"][0]
                tile_y = rock["tile"][1]
                pos_x = rock["pos"][0]
                pos_y = rock["pos"][1]

                if camera:
                    pos_x -= camera.get_position()[0]
                    pos_y -= camera.get_position()[1]

                self._rock_tileset.draw_tile(tile_x, tile_y, pos_x, pos_y)

            # r_x, r_y = (50, 50)
            # r2_x, r2_y = (50, 450)
            # if camera:
            #     r_x -= camera.get_position()[0]
            #     r_y -= camera.get_position()[1]
            #     r2_x -= camera.get_position()[0]
            #     r2_y -= camera.get_position()[1]
            # self._rock_tileset.draw_tile(4, 2, r_x, r_y)
            # self._rock_tileset.draw_tile(4, 2, r2_x, r2_y)
            # #####################################

            # test1 = (10, 200)
            # test2 = (20, 300)
            # print(tuple(set(test1) ^ set(test2)))