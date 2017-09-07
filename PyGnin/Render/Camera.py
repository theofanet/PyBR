import PyGnin
import pygame


class Camera(object):
    def __init__(self, track_zone=(0, 0), speed=1):
        super().__init__()
        self.position = (0, 0)
        self.trackZone = track_zone
        self.viewSize = PyGnin.App.get_screen_size()
        self.speed = speed

    def is_in(self, rect):
        return pygame.Rect(self.position, self.viewSize).colliderect(rect)

    def set_position(self, x=0, y=0):
        self.position = (x, y)

    def get_position(self):
        return [self.position[0], self.position[1]]

    def update(self, position=None, direction=None, max_size=None):
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
