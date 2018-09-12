from .Sprite import Sprite
from ..Render import Image
from ..Core import App


class Animation(object):
    def __init__(self, row=0, cell=0, nb_frame=1, frequency=100, vertical=False, one_time=False):
        super().__init__()
        self._elapsedTime = 0
        self.stopped = False
        self.one_time = one_time
        self.vertical = vertical
        self.start_row = row
        self.start_cell = cell
        self.row = row
        self.cell = cell
        self.nbFrame = nb_frame
        self.frequency = frequency
        self.index = cell if not vertical else row

    def update(self):
        self._elapsedTime += App.get_clock().get_time()
        if not self.stopped:
            start_index = self.start_cell if not self.vertical else self.start_row
            if self._elapsedTime > self.frequency:
                self.index += 1
                self._elapsedTime -= self.frequency
                if self.index > start_index + (self.nbFrame - 1):
                    if self.one_time:
                        self.stopped = True
                        self.index = start_index + (self.nbFrame - 1)
                    else:
                        self.index = start_index
                if self.vertical:
                    self.row = self.index
                else:
                    self.cell = self.index

    def reset(self):
        self.index = self.start_cell if not self.vertical else self.start_row
        self._elapsedTime = 0
        self.stopped = False


class AnimatedSprite(Sprite):
    def __init__(self):
        super().__init__()
        self._index = 1
        self._frameRect = None
        self._playing = False
        self._animations = {}
        self._animation = None
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
                self._frameRect.width * self._animation.cell,
                self._frameRect.height * self._animation.row,
                self._frameRect.width,
                self._frameRect.height
            )
        super().draw(surface, camera)

    def get_frame_rect(self):
        return self._frameRect

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
