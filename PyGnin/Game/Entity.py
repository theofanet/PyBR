import pygame
from .Sprite import Sprite


class Entity(Sprite):
    def __init__(self):
        super().__init__()
        self._bounding_box = pygame.Rect(0, 0, 0, 0)

    def draw(self, surface, camera=None):
        super().draw(surface, camera)
        rect = self.get_bbox()
        if camera:
            rect.x -= camera.position[0]
            rect.y -= camera.position[1]
        pygame.draw.rect(surface, (255, 0, 0), rect)

    def get_bbox(self):
        rect = self._bounding_box.copy()
        rect.x += self.rect.x
        rect.y += self.rect.y
        return rect

    def check_collision(self, entity):
        if entity.get_bbox().colliderect(self.get_bbox()):
            return True
        return False