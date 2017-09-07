import pygame
from ..Registry import Registry
from ..Core import App


class Image(object):

    def __init__(self, path, convert=True):
        self._path = ""
        self._scale = 1
        self._img = pygame.image.load(path)
        if convert:
            self._img.convert()

    def get_img(self):
        return self._img

    def get_rect(self):
        return self._img.get_rect()

    def set_color(self, r, g, b):
        img = self._img.copy()
        img.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        img.fill((r, g, b, 0), None, pygame.BLEND_RGBA_ADD)
        self._img = img
        return self

    def set_scale(self, scale):
        self._scale = scale
        rect = self.get_rect()
        n_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA, 32)
        n_surf = n_surf.convert_alpha(n_surf)
        n_surf.blit(self._img, pygame.Rect(0, 0, rect.width, rect.height))
        size = n_surf.get_size()
        n_surf = pygame.transform.scale(n_surf, (int(size[0] * self._scale), int(size[1] * self._scale)))
        self._img = n_surf
        return self

    def draw(self, x=0, y=0, area=None, at_center=False, display=None):
        if not display:
            display = App.get_display()
            if not display:
                return False
        rect = self._img.get_rect()
        rect.x = x
        rect.y = y
        if at_center:
            w = rect.width
            h = rect.height
            if area is not None:
                w = area.width
                h = area.height
            rect.x -= w / 2
            rect.y -= h / 2
        display.blit(self._img, rect, area)
        return True
