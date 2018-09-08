import PyGnin
from PyGnin import *
import pygame


class Bullet(Game.Sprite):
    def __init__(self, position=(0, 0), direction=(1, 1)):
        super().__init__()
        self.load_image("assets/bullet.png")
        self._life_time = 3000
        self._speed = 10
        self._direction = Game.Vector(direction[0], direction[1])
        self._direction.normalize()
        self.set_position(position[0], position[1])
        self._time = 0

    def update(self, *args):
        x, y = self.get_position()
        self.set_position(x + self._speed*self._direction.x, y + self._speed*self._direction.y)
        self._time += App.get_time()
        super().update(*args)

    def is_destroy(self):
        return self._life_time < self._time

    def destroy(self):
        self._life_time = 0
