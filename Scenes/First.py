from PyGnin import *
import Sprites
from opensimplex import OpenSimplex
import pygame
import time


class Map(object):
    width = 0
    height = 0
    tiles = None

    DEEP_WATER = (62, 96, 193)
    WATER = (93, 128, 253)
    LAND = (191, 210, 175)
    GRASS = (116, 169, 99)

    def __init__(self, width=0, height=0):
        super().__init__()
        self.width = width
        self.height = height

    def get_color(self, e, water=0.1):
        if e < water:
            return int(68*water), int(100*water), int(250*water)
        elif e < water + 0.2:
            return int(68*e), int(100*e), int(250*e)
        elif e < water + 0.3:
            return int(191*e), int(210*e), int(175*e)
        else:
            return int(47 * e), int(201 * e), int(25 * e)

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
                self.tiles[y][x] = self.get_color(e, water_lvl)

    def draw(self, camera=None, surface=None):
        if not self.tiles:
            return None

        if not surface:
            surface = App.get_display()

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
                        pygame.draw.rect(surface, self.tiles[y][x], rect)


class FirstScene(Game.Scene):
    _player = None
    _camera = None
    _map = None
    _showMap = False

    _keyboardRepeat = (400, 30)

    def __init__(self):
        super().__init__()

    def _load_resources(self):
        self._player = Sprites.Player()
        self.add_sprites(self._player)
        self._camera = Render.Camera((200, 200), speed=self._player.get_speed())
        self._map = Map(200, 200)
        self._map.generate(int(time.time()), 2.2, 0.2)
        self.mini_map = pygame.Surface((16 * 200, 16 * 200))
        self._map.draw(None, self.mini_map)
        self.mini_map = pygame.transform.scale(self.mini_map, (self._camera.viewSize[0] - 40, self._camera.viewSize[1] - 40))

    def update(self):
        if IO.Keyboard.is_down(K_m):
            self._showMap = not self._showMap

        if not self._showMap:
            super().update()
            if IO.Mouse.is_held(IO.M_LEFT) and IO.Mouse.is_moving():
                pos = self._camera.get_position()
                pos[0] += IO.Mouse.rel()[0]
                pos[1] += IO.Mouse.rel()[1]
                self._camera.set_position(pos[0], pos[1])

            self._camera.update(self._player.get_position(), self._player.get_direction())

    def draw(self):
        if self._showMap:
            App.get_display().fill((0, 0, 0))
            rect = self.mini_map.get_rect()
            rect.x += 20
            rect.y += 20
            App.get_display().blit(self.mini_map, rect)
            x = (self._player.get_position()[0] / (200*16)) * rect.width
            y = (self._player.get_position()[1] / (200*16)) * rect.height
            pygame.draw.rect(App.get_display(), (255, 0, 0), pygame.Rect(20 + x, 20 + y, 8, 10))
        else:
            self._map.draw(self._camera)
            super().draw_sprites(self._camera)
