import PyGnin
import pygame


class Camera(object):
    def __init__(self, track_zone=(0, 0), speed=1, map_size=(0, 0)):
        super().__init__()
        self.position = (0, 0)
        self.trackZone = track_zone
        self.viewSize = PyGnin.App.get_screen_size()
        self.speed = speed
        self.map_size = map_size

    def is_in(self, rect):
        return pygame.Rect(self.position, self.viewSize).colliderect(rect)

    def set_position(self, x=0, y=0):
        self.position = (x, y)

    def get_position(self):
        return [self.position[0], self.position[1]]

    def center_camera(self, x, y):
        x -= self.viewSize[0] / 2
        y -= self.viewSize[1] / 2
        if x < 0:
            x = 0
        elif x + self.viewSize[0] > self.map_size[0]:
            x = self.map_size[0] - self.viewSize[0]
        if y < 0:
            y = 0
        elif y + self.viewSize[1] > self.map_size[1]:
            y = self.map_size[1] - self.viewSize[1]
        self.set_position(x, y)

    def update(self, position=None, direction=None, max_size=None):
        if not max_size:
            max_size = self.map_size
        pos = self.get_position()
        if 0 < pos[0] and direction and position[0] < self.position[0] + self.trackZone[0]:
            pos[0] -= self.speed
        if (not max_size or pos[0] < (max_size[0] - self.viewSize[0])) and direction \
                and position[0] > self.position[0] + self.viewSize[0] - self.trackZone[0]:
            pos[0] += self.speed
        if 0 < pos[1] and direction and position[1] < self.position[1] + self.trackZone[1]:
            pos[1] -= self.speed
        if (not max_size or pos[1] < (max_size[1] - self.viewSize[1])) and direction \
                and position[1] > self.position[1] + self.viewSize[1] - self.trackZone[1]:
            pos[1] += self.speed
        self.set_position(pos[0], pos[1])
