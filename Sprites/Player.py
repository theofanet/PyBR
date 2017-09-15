import PyGnin
from PyGnin import *
import pygame
from .Bullet import Bullet


class Player(Game.AnimatedSprite):
    def __init__(self, active=True):
        super().__init__()
        self._config = Registry.registered("config")
        self._speed = 5
        self.load_image("assets/mage.png")
        self.set_scale(3)
        self._frameRect.width = 16 * self._scale
        self._frameRect.height = 16 * self._scale
        self.add_animation("run-down", Game.Animation(nb_frame=4))
        self.add_animation("run-up", Game.Animation(nb_frame=4, start_index=4))
        self.add_animation("run-right", Game.Animation(row=1, nb_frame=4))
        self.add_animation("run-left", Game.Animation(row=1, nb_frame=4, start_index=4))
        self.set_animation("run-down")
        self._direction = None
        self._play_size = None
        self._aimPosition = [0, 0]
        self._aims = Render.TileSet("assets/aims.png", (188, 200))
        self._aims.set_scale(self._config.getfloat("aim", "scale"))
        self._aim_color = None
        self.set_aim_color(list(map(int, self._config.get("aim", "color").split(","))))
        self._bullets = []
        self._active = active
        self.bbox = pygame.Rect(6, 5, 34, 39)

    def set_aim_color(self, col):
        self._aims.set_color(col)
        self._aim_color = col

    def update(self, *args):
        if not self._active:
            return

        x, y = self.get_position()

        if App.get_active_scene().get_camera():
            x_cam, y_cam = App.get_active_scene().get_camera().get_position()
        else:
            x_cam, y_cam = (0, 0)

        if IO.Keyboard.is_held(K_a):
            if self._direction != PyGnin.DIR_UP and self._direction != PyGnin.DIR_DOWN:
                self.set_animation("run-left", play=True, reset=self._direction != PyGnin.DIR_LEFT)
                self._direction = PyGnin.DIR_LEFT
            x -= self._speed
        elif IO.Keyboard.is_held(K_d):
            if self._direction != PyGnin.DIR_UP and self._direction != PyGnin.DIR_DOWN:
                self.set_animation("run-right", play=True, reset=self._direction != PyGnin.DIR_RIGHT)
                self._direction = PyGnin.DIR_RIGHT
            x += self._speed

        if IO.Keyboard.is_held(K_w):
            self.set_animation("run-up", play=True, reset=self._direction != PyGnin.DIR_UP)
            self._direction = PyGnin.DIR_UP
            y -= self._speed
        elif IO.Keyboard.is_held(K_s):
            self.set_animation("run-down", play=True, reset=self._direction != PyGnin.DIR_DOWN)
            self._direction = PyGnin.DIR_DOWN
            y += self._speed

        if IO.Keyboard.is_up(K_a) \
                or IO.Keyboard.is_up(K_d) \
                or IO.Keyboard.is_up(K_w)\
                or IO.Keyboard.is_up(K_s):
            self._direction = None
            self.stop_animation(reset=True)

        if 0 > x:
            x = 0
        if self._play_size is not None and x > (self._play_size[0] - self._frameRect.width):
            x = self._play_size[0] - self._frameRect.width
        if 0 > y:
            y = 0
        if self._play_size is not None and y > (self._play_size[1] - self._frameRect.height):
            y = self._play_size[1] - self._frameRect.height

        self.set_position(x, y)
        self.bbox.x = x + 6
        self.bbox.y = y + 5

        self._aimPosition = IO.Mouse.position()
        aim_vector = Game.Vector(self._aimPosition[0] + x_cam - x, self._aimPosition[1] + y_cam - y)
        if aim_vector.length() > self._config.getfloat("aim", "max_length"):
            aim_vector.normalize()
            aim_vector.mult(self._config.getfloat("aim", "max_length"))
        self._aimPosition = [x + aim_vector.x - x_cam, y + aim_vector.y - y_cam]
        aim_angle = aim_vector.angle()
        if aim_angle < 0:
            aim_angle = 360 + aim_angle
        IO.Debug.log("Angle : {0}", aim_angle)
        if 315 < aim_angle or aim_angle < 45:
            self.set_animation("run-down")
        elif 45 < aim_angle < 135:
            self.set_animation("run-right")
        elif 135 < aim_angle < 225:
            self.set_animation("run-up")
        elif 225 < aim_angle < 315:
            self.set_animation("run-left")

        for bullet in self._bullets:
            bullet.update(*args)

        if IO.Mouse.is_down(IO.M_LEFT):
            self.shoot()

        super().update(*args)

    def get_bbox(self):
        return self.bbox

    def draw(self, surface, camera=None):
        x, y = self.get_position()
        x_cam, y_cam = (0, 0)
        aim_pos = self._aimPosition
        if camera:
            x_cam, y_cam = App.get_active_scene().get_camera().get_position()
        if self._config.getboolean("aim", "draw_line"):
            pygame.draw.line(
                surface,
                self._aim_color,
                (x + self._frameRect.width / 2 - x_cam, y + self._frameRect.height / 2 - y_cam),
                aim_pos
            )
        c, r = list(map(int, self._config.get("aim", "type").split(",")))
        self._aims.draw_tile(c, r, aim_pos[0], aim_pos[1], True)

        i = 0
        for bullet in self._bullets:
            bullet.draw(surface, camera)
            if bullet.is_destroy():
                del self._bullets[i]
            i += 1

        x, y, w, h = self.bbox
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(x - x_cam, y - y_cam, w, h), 1)

        super().draw(surface, camera)

    def set_play_size(self, size=(0, 0)):
        self._play_size = size

    def get_direction(self):
        return self._direction

    def get_speed(self):
        return self._speed

    def shoot(self):
        x, y = self.get_position()
        x, y = (x + self._frameRect.width / 2, y + self._frameRect.height / 2)
        aim_x, aim_y = self._aimPosition
        aim_x, aim_y = (aim_x + self._aims.get_tile_size()[0] / 2, aim_y + self._aims.get_tile_size()[1] / 2)
        if App.get_active_scene().get_camera():
            x_cam, y_cam = App.get_active_scene().get_camera().get_position()
        else:
            x_cam, y_cam = (0, 0)
        bullet = Bullet(
            (x, y),
            (aim_x + x_cam - x, aim_y + y_cam - y)
        )
        self._bullets.append(bullet)
