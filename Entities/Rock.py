from PyGnin import *
import pygame


class Rock(Game.Sprite):
    def __init__(self):
        super().__init__()
        self.load_image("assets/rock1.png")
        self.set_scale(0.5)
        self._bounding_box = pygame.Rect(self.rect.w/2 - 20, self.rect.h - 35, self.rect.w - 30, 30)

    def draw(self, surface, camera=None):
        super().draw(surface, camera)
        #rect = self.get_bbox()
        #if camera:
        #    rect.x -= camera.position[0]
        #    rect.y -= camera.position[1]
        #pygame.draw.rect(surface, (255, 0, 0), rect)

    def get_bbox(self):
        rect = self._bounding_box.copy()
        rect.x += self.rect.x
        rect.y += self.rect.y
        return rect

    def check_collision(self, rect):
        if rect.colliderect(self.get_bbox()):
            return True
        return False