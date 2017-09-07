import pygame


class Debug(object):
    _active = True
    _debug_lines = []
    _font = None
    _color = (0, 255, 0)
    _font_size = 26

    @staticmethod
    def init(active=True, font_file=None, font_size=26):
        Debug._active = active
        Debug._font_size = font_size
        if Debug._active:
            if font_file:
                Debug._font = pygame.font.Font(font_file, font_size)
            else:
                Debug._font = pygame.font.SysFont("Lucida Console", font_size)

    @staticmethod
    def log(txt, *args):
        Debug._debug_lines.append(txt.format(*args))

    @staticmethod
    def draw(screen):
        if not Debug._active:
            return None

        x, y = (5, 5)
        for line in Debug._debug_lines:
            txt = Debug._font.render(line, True, Debug._color)
            screen.blit(txt, (x, y))
            y += int(Debug._font_size * 1.2)

        Debug._debug_lines.clear()
