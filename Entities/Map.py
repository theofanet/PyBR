from PyGnin import *
from .Tree import Tree
from .Rock import Rock
from opensimplex import OpenSimplex
from Entities.Rock import *
import pygame
import random


class Map(object):
    def __init__(self, width=0, height=0):
        super().__init__()
        self._font = Render.Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf")
        self.width = width
        self.height = height
        self.tiles = None
        self.tiles_type = None
        self.trees = None
        self._tileSet = Render.TileSet("assets/island.png")
        #self._treeTexture = Render.Image("assets/tree.png")
        self._surfaces = {
            "water": (0, 0),
            "dirt": (4, 2),
            "rock": (2, 0),
            "grass": (5, 0)
        }
        self._size = (width * 16, height * 16)
        self._water_rects = []

        self._mini_map = None

    def get_size(self):
        return self._size

    def get_surface(self, e, water=0.1):
        if e < water:
            return self._surfaces["grass"], "grass"
        elif e < water + 0.3:
            return self._surfaces["grass"], "grass"
        elif e < water + 0.5:
            return self._surfaces["dirt"], "dirt"
        else:
            return self._surfaces["dirt"], "dirt"

    @staticmethod
    def noise(nx, ny, generator):
        return generator.noise2d(nx, ny) / 2.0 + 0.5

    def generate(self, seed=0, frequency=1.0, water_lvl=0.1):
        App.draw_loading("Generating map ...", self._font)
        generator = OpenSimplex(seed=seed)

        self.tiles = [[0 for x in range(self.width)] for y in range(self.height)]
        self.trees = [[0 for x in range(self.width)] for y in range(self.height)]
        self.tiles_type = [["dirt" for x in range(self.width)] for y in range(self.height)]
        App.draw_loading("Generating map : tiles ...", self._font)

        done = 0
        water_w, water_h = (0, 0)
        water_x, water_y = (0, 0)
        is_water = False
        self._water_rects = []
        for y in range(self.height):
            for x in range(self.width):
                nx = x / self.width - 0.5
                ny = y / self.height - 0.5
                e = generator.noise2d(frequency * nx, frequency * ny) / 2.0 + 0.5
                d = self.get_surface(e, water_lvl)
                self.tiles[y][x] = d[0]
                self.tiles_type[y][x] = d[1]
                if self.tiles[y][x] == self._surfaces["water"]:
                    water_w += 16
                    if not is_water:
                        water_x = x * 16
                        water_y = y * 16
                        water_h += 16
                    is_water = True
                elif is_water:
                    self._water_rects.append(pygame.Rect(water_x, water_y, water_w, water_h))
                    water_w, water_h = (0, 0)
                    is_water = False
                done += 1
                #App.draw_loading("Generating tiles ({0}/{1}) ...".format(done, to_do))

        for y in range(self.height):
            for x in range(self.width):
                r = random.random()
                if r > 0.998:
                    if self.tiles_type[y][x] == "dirt":
                        rock = Rock()
                        rock.set_position(16 * x, 16 * y)
                        self.trees[y][x] = rock
                    else:
                        tree = Tree()
                        tree.set_position((16 * x) - tree.rect.w / 2, (16 * y) - tree.rect.h)
                        self.trees[y][x] = tree

        # Mini map generation
        App.draw_loading("Generating map : mini map ...", self._font)
        self._mini_map = pygame.Surface((16 * self.width, 16 * self.height))
        self.draw(camera=None, surface=self._mini_map)
        self.draw_foreground(camera=None, surface=self._mini_map)
        self._mini_map = pygame.transform.scale(self._mini_map, (
            App.get_screen_size()[0] - 40,
            App.get_screen_size()[1] - 40
        ))

    def get_tile_coords(self, tile_type, x, y):
        A = False
        B = False
        C = False
        D = False
        AB = False
        BC = False
        CD = False
        AD = False

        if y > 0 and self.tiles_type[y - 1][x] != tile_type:
            A = True
        if x < self.width - 1 and self.tiles_type[y][x + 1] != tile_type:
            B = True
        if y < self.height - 1 and self.tiles_type[y + 1][x] != tile_type:
            C = True
        if x > 0 and self.tiles_type[y][x - 1] != tile_type:
            D = True
        if y > 0 and x < self.width - 1 and self.tiles_type[y - 1][x + 1] != tile_type:
            AB = True
        if y < self.height - 1 and x < self.width - 1 and self.tiles_type[y + 1][x + 1] != tile_type:
            BC = True
        if y < self.height - 1 and x > 0 and self.tiles_type[y + 1][x - 1] != tile_type:
            CD = True
        if y > 0 and x > 0 and self.tiles_type[y - 1][x - 1] != tile_type:
            AD = True

        if A and not B and not C and not D:
            return self._surfaces[tile_type][0] + 1, self._surfaces[tile_type][1]
        if B and not A and not C and not D:
            return self._surfaces[tile_type][0] + 2, self._surfaces[tile_type][1] + 1
        if C and not A and not B and not D:
            return self._surfaces[tile_type][0] + 1, self._surfaces[tile_type][1] + 2
        if D and not A and not B and not C:
            return self._surfaces[tile_type][0], self._surfaces[tile_type][1] + 1
        if A and B and not C and not D:
            return self._surfaces[tile_type][0] + 2, self._surfaces[tile_type][1]
        if A and not B and not C and D:
            return self._surfaces[tile_type][0], self._surfaces[tile_type][1]
        if B and not A and C and not D:
            return self._surfaces[tile_type][0] + 2, self._surfaces[tile_type][1] + 2
        if C and not A and not B and D:
            return self._surfaces[tile_type][0], self._surfaces[tile_type][1] + 2
        if AB and not BC and not CD and not AD:
            return self._surfaces[tile_type][0] + 3, self._surfaces[tile_type][1] + 1
        if not AB and BC and not CD and not AD:
            return self._surfaces[tile_type][0] + 3, self._surfaces[tile_type][1]
        if not AB and not BC and CD and not AD:
            return self._surfaces[tile_type][0] + 4, self._surfaces[tile_type][1]
        if not AB and not BC and not CD and AD:
            return self._surfaces[tile_type][0] + 4, self._surfaces[tile_type][1] + 1

        return self._surfaces[tile_type][0] + 1, self._surfaces[tile_type][1] + 1

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

    def draw_foreground(self, camera=None, surface=None):
            x_start = 0
            x_end = self.width
            y_start = 0
            y_end = self.height

            if not surface:
                surface = App.get_display()

            if camera:
                view_offset = 10
                x_start = int(camera.position[0] / 16) - view_offset
                y_start = int(camera.position[1] / 16) - view_offset
                x_end = x_start + int(camera.viewSize[0] / 16) + view_offset
                y_end = y_start + int(camera.viewSize[1] / 16) + view_offset

            #g_rect = self._treeTexture.get_img().get_rect()
            for y in range(y_start, y_end):
                if 0 <= y < len(self.tiles):
                    for x in range(x_start, x_end):
                        if 0 <= x < len(self.tiles[y]):
                            rect = pygame.Rect(16 * x, 16 * y, 16, 16)
                            if camera:
                                rect.x -= camera.get_position()[0]
                                rect.y -= camera.get_position()[1]
                            #if self.trees[y][x] == 1:
                                #rect.x -= g_rect.width / 2
                                #rect.y -= g_rect.height
                                #self._treeTexture.draw(rect.x, rect.y, display=surface)
                            if self.trees[y][x]:
                                self.trees[y][x].draw(camera=camera, surface=surface)


    def check_water_collision(self, player, camera=None):
            x_start = 0
            x_end = self.width
            y_start = 0
            y_end = self.height

            if camera:
                view_offset = 10
                x_start = int(camera.position[0] / 16) - view_offset
                y_start = int(camera.position[1] / 16) - view_offset
                x_end = x_start + int(camera.viewSize[0] / 16) + view_offset
                y_end = y_start + int(camera.viewSize[1] / 16) + view_offset

            player_bbox = player.get_bbox()
            for y in range(y_start, y_end):
                if 0 <= y < len(self.tiles):
                    for x in range(x_start, x_end):
                        if 0 <= x < len(self.tiles[y]):
                            if self.trees[y][x] and self.trees[y][x] != 2:
                                if self.trees[y][x].check_collision(player_bbox):
                                    return True
