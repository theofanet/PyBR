from PyGnin import *
import pygame


class Tree(Game.Sprite):
    def __init__(self):
        super().__init__()
        self.load_image("assets/tree.png")
        self._bounding_box = pygame.Rect(self.rect.w/2 - 10, self.rect.h - 20, 20, 10)

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
        print("CHECK")
        if rect.colliderect(self.get_bbox()):
            return True
        return False