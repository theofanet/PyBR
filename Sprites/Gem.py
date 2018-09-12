import PyGnin
from PyGnin import *
import pygame
import random


GEM_COLORS = [
    "blue",
    "green",
    "purple",
    "orange",
    "yellow",
    "red"
]


class Gem(Game.Sprite):
    def __init__(self, points=None, json_data=None):
        super().__init__()
        if not json_data:
            if points is None:
                points = random.randint(0, len(GEM_COLORS) - 1)
            else:
                if 1 > points:
                    points = 1
                elif points > len(GEM_COLORS):
                    points = len(GEM_COLORS)
        else:
            if "points" in json_data:
                points = json_data["points"]
            if "position" in json_data:
                self.set_position(json_data["position"][0], json_data["position"][1])
        self._points = points
        self._color = GEM_COLORS[self._points-1]
        self.load_image("assets/gem_"+self._color+".png")
        self._bounding_box = pygame.Rect(0, 0, self.rect.width, self.rect.height)

    def update(self, *args):
        super().update(*args)

    def get_points(self):
        return self._points

    def get_bbox(self):
        rect = self._bounding_box.copy()
        rect.x += self.rect.x
        rect.y += self.rect.y
        return rect

    def to_json(self):
        return {
            "points": self._points,
            "position": self.get_position()
        }
