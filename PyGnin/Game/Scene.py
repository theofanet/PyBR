from ..Core import App
from ..Render import Image
import pygame


class SpriteGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def cam_draw(self, surface, camera=None):
        sprites = self.sprites()
        for spr in sprites:
            self.spritedict[spr] = spr.draw(surface, camera)
        self.lostsprites = []


class Scene(object):
    _images = {}
    _keyboardRepeat = None
    _sprites = None

    def __init__(self):
        super().__init__()
        self._images = {}
        self._sprites = SpriteGroup()

    def update(self):
        self._sprites.update()

    def draw(self):
        self.draw_sprites()

    def draw_sprites(self, camera=None):
        self._sprites.cam_draw(App.get_display(), camera)

    def load_image(self, path, convert=True, key=None):
        if not key or key not in self._images:
            img = Image(path, convert)
            if key:
                self._images[key] = img
            return img
        elif key:
            return self._images

    def get_image(self, key):
        if key in self._images:
            return self._images[key]

    def activate(self):
        self._load_resources()
        if self._keyboardRepeat:
            pygame.key.set_repeat(self._keyboardRepeat[0], self._keyboardRepeat[1])

    def _load_resources(self): pass

    def add_sprites(self, *sprites):
        self._sprites.add(*sprites)
