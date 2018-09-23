import pygame
from ..Core import App


class Font(object):
    def __init__(self, font_file, size=26, color=(255, 255, 255)):
        self._color = color
        self._font = pygame.font.Font(font_file, size)

    def set_color(self, color):
        self._color = color
        return self

    def draw_text(self, text, position=(0, 0), color=False, screen=False, update_display=False, center_x=False, center_y=False):
        if not screen:
            screen = App.get_display()
        if not color:
            color = self._color
        txt = self._font.render(text, True, color)
        if center_x or center_y:
            x, y = position
            if center_x:
                x -= txt.get_rect().width / 2
            if center_y:
                y -= txt.get_rect().height / 2
            position = (x, y)
        screen.blit(txt, position)
        if update_display:
            pygame.display.update()
