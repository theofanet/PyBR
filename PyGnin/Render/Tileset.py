import pygame
from .Image import Image
from ..Core import App


class TileSet(object):
    def __init__(self, image_path, tile_size=(16, 16)):
        self._image = Image(image_path)
        self._tileSize = tile_size

    def set_scale(self, scale):
        self._image.set_scale(scale)
        self._tileSize = (int(self._tileSize[0]*scale), int(self._tileSize[1]*scale))

    def set_color_rgb(self, r, g, b):
        self._image.set_color(r, g, b)
        return self

    def set_color(self, color=(255, 255, 255)):
        return self.set_color_rgb(color[0], color[1], color[2])

    def get_color(self):
        return self._image.get_color()

    def get_tile_size(self):
        return self._tileSize

    def draw_tile(self, col, row, x, y, at_center=False, screen=None):
        if not screen:
            screen = App.get_display()
        self._image.draw(x, y, pygame.Rect(
            col*self._tileSize[1],
            row*self._tileSize[0],
            self._tileSize[0],
            self._tileSize[1]
        ), at_center=at_center, display=screen)
