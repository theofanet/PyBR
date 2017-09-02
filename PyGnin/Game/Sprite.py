import pygame
from ..Render.Image import Image


class Sprite(pygame.sprite.Sprite):
    rect = None
    area = None
    image = None
    _scale = 1
    _image = None

    def __init__(self):
        super().__init__()

    def load_image(self, path):
        self._image = Image(path)
        self.image = self._image.get_img()
        self.rect = self.image.get_rect()

    def set_position(self, x=None, y=None):
        if x:
            self.rect.x = x
        if y:
            self.rect.y = y

    def get_position(self):
        return self.rect.x, self.rect.y

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

    def draw(self, surface, camera=None):
        if self.image:
            rect = self.rect.copy()

            if camera:
                rect.x -= camera.position[0]
                rect.y -= camera.position[1]

                if not camera.is_in(self.rect):
                    return None

            n_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA, 32)
            n_surf = n_surf.convert_alpha(n_surf)
            n_surf.blit(self.image, pygame.Rect(0, 0, rect.width, rect.height), self.area)
            size = n_surf.get_size()
            n_surf = pygame.transform.scale(n_surf, (size[0] * self._scale, size[1] * self._scale))

            return surface.blit(n_surf, rect)
