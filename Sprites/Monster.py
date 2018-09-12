import PyGnin
from PyGnin import *
import pygame
import math


class Monster(Game.AnimatedSprite):
    def __init__(self, active=True, json_data=None):
        super().__init__()
        self._config = Registry.registered("config")
        self._speed = 5
        self.load_image("assets/players3.png")
        self._frameRect.width = 32 * self._scale
        self._frameRect.height = 32 * self._scale
        self.add_animation("run-down", Game.Animation(cell=9, row=0, nb_frame=3))
        self.add_animation("run-up", Game.Animation(cell=9, row=3, nb_frame=3))
        self.add_animation("run-right", Game.Animation(cell=9, row=2, nb_frame=3))
        self.add_animation("run-left", Game.Animation(cell=9, row=1, nb_frame=3))
        self.set_animation("run-down")
        self._active_animation = "run-down"
        self._direction = None
        self._play_size = None
        self._active = active
        self.bbox = pygame.Rect(10, 5, 12, 25)
        self._path = []
        self._master_path = []
        self._loop_path = False
        self._run_path = False
        self._current_path_index = 0
        self._time = 0
        self._go_to = (0, 0)

        if json_data:
            if "position" in json_data:
                self.set_position(json_data["position"][0], json_data["position"][1])
            if "path" in json_data:
                self.launch_path(json_data["path"]["path"], loop=json_data["path"]["loop"])

    def set_position(self, x=None, y=None):
        if x:
            self.rect.x = x
            self.bbox.x = x + 10
        if y:
            self.rect.y = y
            self.bbox.y = y + 8

    def launch_path(self, path, loop=False):
        self._path = path
        self._master_path = self._path.copy()
        self._loop_path = loop
        self._run_path = True
        x, y = self._path.pop(0)
        self.set_position(x*16, y*16)
        x, y = self._path.pop(0)
        self._go_to = (x*16, y*16)
        self._time = 0

    def loop_current_path(self):
        if not self._loop_path:
            return None
        self._path = self._master_path.copy()
        x, y = self._path.pop(0)
        self._go_to = (x*16, y*16)

    def normalise(self, x, y):
        mag = math.sqrt(x*x + y*y)
        nx = x / mag if mag > 0 else x
        ny = y / mag if mag > 0 else y
        return nx, ny

    def length(self, x, y):
        return math.sqrt(x*x + y*y)

    def update(self, *args):
        super().update(*args)
        if self._run_path:
            self._time += App.get_time()
            x, y = self.get_position()
            gx, gy = self._go_to
            dx, dy = (gx - x, gy - y)
            if self.length(dx, dy) > 3:
                nx, ny = self.normalise(dx, dy)
                nx = 0 if nx == 0 else (1 if nx > 0 else -1)
                ny = 0 if ny == 0 else (1 if ny > 0 else -1)
                if nx != 0 or ny != 0:
                    animation = "run-down"
                    if nx > 0:
                        animation = "run-right"
                    elif nx < 0:
                        animation = "run-left"
                    if ny > 0:
                        animation = "run-down"
                    elif ny < 0:
                        animation = "run-up"
                    if animation != self._active_animation:
                        self.set_animation(animation, play=True)
                        self._active_animation = animation
                else:
                    self.stop_animation()

                self.set_position(math.ceil(x+nx), math.ceil(y+ny))
            elif len(self._path):
                px, py = self._path.pop(0)
                self._go_to = (px*16, py*16)
            else:
                if not self._loop_path:
                    self._run_path = False
                else:
                    self.loop_current_path()

    def get_bbox(self):
        return self.bbox

    def draw(self, surface, camera=None):
        # x, y, w, h = self.bbox
        # pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(x - x_cam, y - y_cam, w, h), 1)
        super().draw(surface, camera)

    def set_play_size(self, size=(0, 0)):
        self._play_size = size

    def get_direction(self):
        return self._direction

    def get_speed(self):
        return self._speed

    def to_json(self):
        return {
            "position": self.get_position(),
            "path": {
                "loop": self._loop_path,
                "path": self._master_path
            }
        }