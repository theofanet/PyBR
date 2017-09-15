from PyGnin import *
from opensimplex import OpenSimplex
from Entities.Rock import *
import pygame
import math


class Map(object):
    def __init__(self, width=0, height=0, seed=0, frequency=1.0, water_lvl=0.1):
        super().__init__()
        self._font = Render.Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf")
        App.draw_loading("Generating map ...", self._font)

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
        self._size = (width * 16, height * 16)
        self._water_rects = []

        # Rocks ###############################
        # self._rocks = Rock(40)
        self._optimizer = None
        if Registry.registered("config").getboolean("map", "load_rocks"):
            self._optimizer = Optimizer(self._size)
        # #####################################

        self._mini_map = None
        self.generate(seed, frequency, water_lvl)

    def get_size(self):
        return self._size

    def get_surface(self, e, water=0.1):
        if e < water:
            return self._surfaces["water"]
        elif e < water + 0.3:
            return self._surfaces["grass"]
        elif e < water + 0.5:
            return self._surfaces["dirt"]
        else:
            return self._surfaces["rock"]

    @staticmethod
    def noise(nx, ny, generator):
        return generator.noise2d(nx, ny) / 2.0 + 0.5

    def generate(self, seed=0, frequency=1.0, water_lvl=0.1):
        generator = OpenSimplex(seed=seed)

        self.tiles = [[0 for x in range(self.width)] for y in range(self.height)]
        App.draw_loading("Generating map : tiles ...", self._font)

        done = 0
        to_do = self.width*self.height
        water_w, water_h = (0, 0)
        water_x, water_y = (0, 0)
        is_water = False
        self._water_rects = []
        for y in range(self.height):
            for x in range(self.width):
                nx = x / self.width - 0.5
                ny = y / self.height - 0.5
                e = generator.noise2d(frequency * nx, frequency * ny) / 2.0 + 0.5
                self.tiles[y][x] = self.get_surface(e, water_lvl)
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

        # Rocks ###############################
        if self._optimizer:
            App.draw_loading("Generating map : rocks ...", self._font)
            self._optimizer.generate()
        # self._rocks.generate()
        # #####################################

        # Mini map generation
        App.draw_loading("Generating map : mini map ...", self._font)
        self._mini_map = pygame.Surface((16 * self.width, 16 * self.height))
        self.draw(camera=None, surface=self._mini_map)
        self._mini_map = pygame.transform.scale(self._mini_map, (
            App.get_screen_size()[0] - 40,
            App.get_screen_size()[1] - 40
        ))

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
            # self._rocks.draw(surface=surface, camera=camera)

            # Oprimizer ##########################
            if self._optimizer:
                self._optimizer.draw(surface=surface, camera=camera)

            x, y = player_position
            x_cam, y_cam = (0, 0)
            if camera:
                x_cam, y_cam = camera.get_position()
            x = 16 * math.floor((x+16/2)/16)
            y = 16 * math.floor((y+16/2)/16)
            check_tiles = [
                (x, y),
                (x-16, y),
                (x+16, y),
                (x+32, y),
                (x+48, y),
                (x, y+16),
                (x-16, y+16),
                (x+16, y+16),
                (x+32, y+16),
                (x+48, y+16),
                (x, y+32),
                (x-16, y+32),
                (x+16, y+32),
                (x+32, y+32),
                (x+48, y+32)
            ]
            for (x_tile, y_tile) in check_tiles:
                col = (0, 255, 0)
                print(x_tile, y_tile)
                if self.tiles[int(y_tile/16)][int(x_tile/16)] == self._surfaces["water"]:
                    col = (255, 0, 0)
                pygame.draw.rect(surface, col, pygame.Rect(x_tile - x_cam, y_tile - y_cam, 16, 16))


# TODO : Optimizer n'est pas un sprite. C'est un objet non physique qui utilise une algo pour placer des objets.
# TODO : De ce fait elle ne doit pas etendre de Game.Sprite
# TODO : mais tout simplement de object (class par defaut des objets python)
# TODO : C'est la class Optimizer qui doit completement generer les rocks. Donc tout les tests de collisions et de
# TODO : positionnement des rocks doivent etre faits dans Optimizer. Et ta classe Rock represente un seul rock.
# TODO : Mais ils doivent utiliser la meme texture et pas en instancier une chacun. (Donc utilite du Registry)
# TODO : Grace a l'integration des fonction de generation et de tests dans Optimizer,
# TODO : tu pouras encore reduire les parcours je pense
class Optimizer(Game.Sprite):

    def __init__(self, size):
        super(Optimizer, self).__init__()
        self._surface = App.get_display()
        self._size = size
        self._rects = [{"pos": [0, 0], "size": [0, 0]} for x in range(4)]

        self._items = list()
        self.generate()

    def generate(self):
        default_w = int(self._size[0] / 2)
        default_h = int(self._size[1] / 2)

        self._rects[0]["pos"][0] = 0
        self._rects[0]["pos"][1] = 0
        self._rects[0]["size"][0] = default_w
        self._rects[0]["size"][1] = default_h

        self._items.append(Rock(10, x=(1, default_w), y=(1, default_w)))

        self._rects[1]["pos"][0] = default_w
        self._rects[1]["pos"][1] = 0
        self._rects[1]["size"][0] = default_w
        self._rects[1]["size"][1] = default_h

        self._items.append(Rock(10, x=(default_w, default_w*2), y=(1, default_w)))

        self._rects[2]["pos"][0] = 0
        self._rects[2]["pos"][1] = default_h
        self._rects[2]["size"][0] = default_w
        self._rects[2]["size"][1] = default_h

        self._items.append(Rock(10, x=(1, default_w), y=(default_w, default_w*2)))

        self._rects[3]["pos"][0] = default_w
        self._rects[3]["pos"][1] = default_h
        self._rects[3]["size"][0] = default_w
        self._rects[3]["size"][1] = default_h

        self._items.append(Rock(10, x=(default_w, default_w*2), y=(default_w, default_w*2)))

        for item in self._items:
            item.generate()

    def draw(self, surface, camera=None):
        for item in self._items:
            item.draw(surface=surface, camera=camera)

        for rect in self._rects:

            pos_x = rect["pos"][0]
            pos_y = rect["pos"][1]

            if camera:
                pos_x -= camera.get_position()[0]
                pos_y -= camera.get_position()[1]

            pygame.draw.rect(surface, (255, 0, 0),
                             (pos_x, pos_y, rect["size"][0], rect["size"][1]), 2)
