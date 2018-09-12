import PyGnin
from PyGnin import *
import pygame
import random
from .Gem import Gem


MAX_GEMS = 20
MIN_GEMS = 5

class Chest(Game.AnimatedSprite):
    def __init__(self, nb_gems=None, json_data=None):
        super().__init__()
        self.load_image("assets/chests.png")
        self._frameRect.width = 32 * self._scale
        self._frameRect.height = 32 * self._scale
        self.add_animation("idle", Game.Animation(row=4))
        self.add_animation("open", Game.Animation(row=4, nb_frame=4, vertical=True, one_time=True))
        self.set_animation("idle")
        self._is_open = False
        self._bounding_box = pygame.Rect(
            0,
            self._frameRect.height * 0.25,
            self._frameRect.width,
            self._frameRect.height * 0.20
        )
        self._open_bbox = pygame.Rect(
            -3,
            -1,
            self._frameRect.width + 3,
            self._frameRect.height + 1
        )
        self._gems = []
        if not json_data:
            if nb_gems is None:
                self._nb_gems = random.randint(MIN_GEMS, MAX_GEMS)
            else:
                self._nb_gems = nb_gems
            for _ in range(0, self._nb_gems - 1):
                gem = Gem()
                self._gems.append(gem)
        else:
            if "position" in json_data:
                self.set_position(json_data["position"][0], json_data["position"][1])
            if "is_open" in json_data:
                self._is_open = json_data["is_open"]
            if "gems" in json_data:
                for g in json_data["gems"]:
                    gem = Gem(json_data=g)
                    self._gems.append(gem)
                self._nb_gems = len(self._gems)

    def update(self, *args):
        super().update(*args)

    def get_bbox(self, open_bbox=False):
        if open_bbox:
            rect = self._open_bbox.copy()
        else:
            rect = self._bounding_box.copy()
        rect.x += self.rect.x
        rect.y += self.rect.y
        return rect

    def draw(self, surface, camera=None):
        super().draw(surface, camera)

        for gem in self._gems:
            gem.draw(surface, camera)

    def set_position(self, x=None, y=None):
        super().set_position(x - self._frameRect.width/2, y-self._frameRect.height/2)

    def check_collision(self, player_bbox, open_bbox=False):
        return player_bbox.colliderect(self.get_bbox(open_bbox))

    def check_gem_collisions(self, player_bbox):
        points = 0
        to_remove = []
        for gem in self._gems:
            if player_bbox.colliderect(gem.get_bbox()):
                points += gem.get_points()
                to_remove.append(gem)
        for gem in to_remove:
            self._gems.remove(gem)
        return points

    def is_open(self):
        return self._is_open

    def open(self):
        self.set_animation("open", play=True)
        self._is_open = True
        for gem in self._gems:
            x, y = self.get_position()
            gem.set_position(x + random.randint(-2, 2)*self._frameRect.width, y + random.randint(-2, 2)*self._frameRect.height)

    def to_json(self):
        data = {
            "position": self.get_position(),
            "is_open": self.is_open(),
            "gems": []
        }
        for gem in self._gems:
            data["gems"].append(gem.to_json())
        return data