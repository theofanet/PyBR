from .Sprite import Sprite
from ..Render import Image
from ..Core import App


class Animation(object):
    row = 0
    startIndex = 0
    nbFrame = 1
    index = 0
    frequency = 0
    active = True
    _elapsedTime = 0

    def __init__(self, row=0, start_index=0, nb_frame=1, frequency=100):
        super().__init__()
        self.row = row
        self.startIndex = start_index
        self.nbFrame = nb_frame
        self.frequency = frequency
        self.index = start_index

    def update(self):
        self._elapsedTime += App.get_clock().get_time()
        if self._elapsedTime > self.frequency:
            self.index += 1
            self._elapsedTime -= self.frequency
            if self.index > self.startIndex + (self.nbFrame - 1):
                self.index = self.startIndex

    def reset(self):
        self.index = self.startIndex


class AnimatedSprite(Sprite):
    _frameRect = None
    _playing = False
    _animations = {}
    _animation = None

    def __init__(self):
        super().__init__()
        self._index = 1
        if self.image:
            self._frameRect = self.image.get_rect()

    def load_image(self, path):
        super().load_image(path)
        self._frameRect = self.rect

    def set_scale(self, scale):
        super().set_scale(scale)
        self._frameRect = self.rect

    def draw(self, surface, camera=None):
        if self._animation:
            self.set_area(
                self._frameRect.width * self._animation.index,
                self._frameRect.height * self._animation.row,
                self._frameRect.width,
                self._frameRect.height
            )
        super().draw(surface, camera)

    def update(self, *args):
        if self._animation and self._playing:
            self._animation.update()
        super().update(*args)

    def add_animation(self, key, animation):
        self._animations[key] = animation

    def stop_animation(self, reset=False):
        if reset and self._animation:
            self._animation.reset()
        self._playing = False

    def set_animation(self, key, play=False, reset=False):
        if key in self._animations:
            self._animation = self._animations[key]
            if reset:
                self._animation.reset()
            if play:
                self._playing = True
