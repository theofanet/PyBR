from PyGnin import *
from opensimplex import OpenSimplex
from Entities.Rock import *
import pygame


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
        self._size = (width * 16, height * 16)

        # Rocks ###############################
        # self._rocks = Rock(40)
        self._optimizer = Optimizer(self._size)
        # #####################################

        self.generate(seed, frequency, water_lvl)
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
        self._optimizer.generate()
        # self._rocks.generate()
        # #####################################

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

            # Oprimizer ###########################
            self._optimizer.draw(surface=surface, camera=camera)


# TODO : Optimizer n'est pas un sprite. C'est un objet non physique qui utilise une algo pour placer des objets.
# TODO :De ce fait elle ne doit pas etendre de Game.Sprite mais tout simplement de object (class par defaut des objets python)
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

        self._items.append(Rock(20, x=(1, default_w), y=(1, default_w)))

        self._rects[1]["pos"][0] = default_w
        self._rects[1]["pos"][1] = 0
        self._rects[1]["size"][0] = default_w
        self._rects[1]["size"][1] = default_h

        self._items.append(Rock(20, x=(default_w, default_w*2), y=(1, default_w)))

        self._rects[2]["pos"][0] = 0
        self._rects[2]["pos"][1] = default_h
        self._rects[2]["size"][0] = default_w
        self._rects[2]["size"][1] = default_h

        self._items.append(Rock(20, x=(1, default_w), y=(default_w, default_w*2)))

        self._rects[3]["pos"][0] = default_w
        self._rects[3]["pos"][1] = default_h
        self._rects[3]["size"][0] = default_w
        self._rects[3]["size"][1] = default_h

        self._items.append(Rock(20, x=(default_w, default_w*2), y=(default_w, default_w*2)))

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