import pygame
from ..Render.Image import Image
from ..Registry import Registry


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = None
        self.area = None
        self.image = None
        self._scale = 1
        self._image = None
        self.draw_size = None

    def load_image(self, path):
        key = "img::" + path
        if not Registry.has(key):
            Registry.register(key, Image(path))
        self._image = Registry.registered(key)
        self.image = self._image.get_img()
        self.rect = self.image.get_rect()

    def set_position(self, x=None, y=None):
        if x:
            self.rect.x = x
        if y:
            self.rect.y = y

    def get_position(self):
        return self.rect.x, self.rect.y

    def get_bbox(self):
        return self.rect

    def set_area(self, x=0, y=0, w=0, h=0):
        if not self.area:
            self.area = pygame.Rect(x, y, w, h)
        else:
            self.area.x = x
            self.area.y = y
            self.area.width = w
            self.area.height = h

    def set_scale(self, scale):
        self._scale = scale
        n_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA, 32)
        n_surf = n_surf.convert_alpha(n_surf)
        n_surf.blit(self.image, pygame.Rect(0, 0, self.rect.width, self.rect.height))
        size = n_surf.get_size()
        # n_surf = pygame.transform.scale(n_surf, (size[0] * self._scale, size[1] * self._scale))
        n_surf = pygame.transform.scale(n_surf, (int(size[0] * self._scale), int(size[1] * self._scale)))
        self.image = n_surf
        self.rect = self.image.get_rect()

    def draw(self, surface, camera=None):
        if self.image:
            rect = self.rect.copy()

            if camera:
                rect.x -= camera.position[0]
                rect.y -= camera.position[1]

                if not camera.is_in(self.rect):
                    return None

            return surface.blit(self.image, rect, self.area)
