import PyGnin
from PyGnin import *
import pygame


class Doors(Game.AnimatedSprite):
    def __init__(self):
        super().__init__()
        self.load_image("assets/doors.png")
        self._frameRect.width = 96 * self._scale
        self._frameRect.height = 64 * self._scale
        self.add_animation("idle", Game.Animation())
        self.add_animation("open-door", Game.Animation(nb_frame=4, vertical=True, one_time=True, frequency=300))
        self.set_animation("idle")
        self._is_open = False
        self._bounding_box = pygame.Rect(
            self._frameRect.width * 0.25,
            0,
            self._frameRect.width * 0.5,
            self._frameRect.height * 0.20
        )
        self._opening_bbox = pygame.Rect(0, 0, self._frameRect.width, self._frameRect.height)

    def get_bbox(self, opening=False):
        if opening:
            rect = self._opening_bbox.copy()
        else:
            rect = self._bounding_box.copy()
        rect.x += self.rect.x
        rect.y += self.rect.y
        return rect

    def set_position(self, x=None, y=None):
        super().set_position(x - self._frameRect.width/2, y-self._frameRect.height/2)

    def check_collision(self, player_bbox, opening=False):
        return player_bbox.colliderect(self.get_bbox(opening))

    def is_open(self):
        return self._is_open

    def open(self):
        self.set_animation("open-door", play=True, reset=True)
        self._is_open = True

    def close(self):
        self.set_animation("idle", reset=True)
        self._is_open = False