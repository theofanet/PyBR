import PyGnin
from PyGnin import *


class Player(Game.AnimatedSprite):
    _speed = 5
    _direction = None

    def __init__(self):
        super().__init__()
        self.load_image("assets/mage.png")
        self._frameRect.width = 16
        self._frameRect.height = 16
        self.add_animation("run-down", Game.Animation(nb_frame=4))
        self.add_animation("run-up", Game.Animation(nb_frame=4, start_index=4))
        self.add_animation("run-right", Game.Animation(row=1, nb_frame=4))
        self.add_animation("run-left", Game.Animation(row=1, nb_frame=4, start_index=4))
        self.set_animation("run-down")
        self._direction = None
        self.set_scale(5)

    def update(self, *args):
        x, y = self.get_position()

        if IO.Keyboard.is_held(K_LEFT):
            if self._direction != PyGnin.DIR_UP and self._direction != PyGnin.DIR_DOWN:
                self.set_animation("run-left", play=True, reset=self._direction != PyGnin.DIR_LEFT)
                self._direction = PyGnin.DIR_LEFT
            x -= self._speed
        elif IO.Keyboard.is_held(K_RIGHT):
            if self._direction != PyGnin.DIR_UP and self._direction != PyGnin.DIR_DOWN:
                self.set_animation("run-right", play=True, reset=self._direction != PyGnin.DIR_RIGHT)
                self._direction = PyGnin.DIR_RIGHT
            x += self._speed

        if IO.Keyboard.is_held(K_UP):
            self.set_animation("run-up", play=True, reset=self._direction != PyGnin.DIR_UP)
            self._direction = PyGnin.DIR_UP
            y -= self._speed
        elif IO.Keyboard.is_held(K_DOWN):
            self.set_animation("run-down", play=True, reset=self._direction != PyGnin.DIR_DOWN)
            self._direction = PyGnin.DIR_DOWN
            y += self._speed

        if IO.Keyboard.is_up(K_LEFT) \
                or IO.Keyboard.is_up(K_RIGHT) \
                or IO.Keyboard.is_up(K_UP)\
                or IO.Keyboard.is_up(K_DOWN):
            self._direction = None
            self.stop_animation(reset=True)

        self.set_position(x, y)

        super().update(*args)

    def get_direction(self):
        return self._direction

    def get_speed(self):
        return self._speed
