import pygame
from ..Registry import Registry
from ..Core import App


class Image(object):
    _path = ""
    _img = None

    def __init__(self, path, convert=True):
        self._img = pygame.image.load(path)
        if convert:
            self._img.convert()

    def get_img(self):
        return self._img

    def get_rect(self):
        return self._img.get_rect()

    def draw(self, x=0, y=0, display=None):
        if not display:
            display = App.get_display()
            if not display:
                return False

        rect = self._img.get_rect()
        rect.x = x
        rect.y = y
        display.blit(self._img, rect)

        return True
