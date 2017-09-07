from pygame.locals import *
import pygame


M_LEFT = 1
M_MIDDLE = 2
M_RIGHT = 3
M_WHEEL_UP = 4
M_WHEEL_DOWN = 5


class Mouse(object):
    _btnDown = {}
    _btnUp = {}
    _btnHeld = {}
    _position = (0, 0)
    _rel = (0, 0)
    _moving = False

    @staticmethod
    def update(event):
        Mouse._moving = False

        if event.type == MOUSEBUTTONUP:
            Mouse._position = event.pos
            Mouse._btnDown[event.button] = True
            if event.button in Mouse._btnDown:
                del Mouse._btnDown[event.button]
            if event.button in Mouse._btnHeld:
                del Mouse._btnHeld[event.button]

        if event.type == MOUSEBUTTONDOWN:
            Mouse._position = event.pos
            Mouse._btnDown[event.button] = True
            Mouse._btnHeld[event.button] = True
            if event.button in Mouse._btnUp:
                del Mouse._btnUp[event.button]

        if event.type == MOUSEMOTION:
            Mouse._moving = True
            Mouse._position = event.pos
            Mouse._rel = event.rel

    @staticmethod
    def is_up(btn):
        if btn in Mouse._btnUp and Mouse._btnUp[btn]:
            del Mouse._btnUp[btn]
            return True
        return False

    @staticmethod
    def is_down(btn):
        if btn in Mouse._btnDown and Mouse._btnDown[btn]:
            del Mouse._btnDown[btn]
            return True
        return False

    @staticmethod
    def is_held(btn):
        if btn in Mouse._btnHeld and Mouse._btnHeld[btn]:
            return True
        return False

    @staticmethod
    def position():
        return Mouse._position

    @staticmethod
    def set_position(position=(0, 0)):
        pygame.mouse.set_pos(position[0], position[1])

    @staticmethod
    def rel():
        return Mouse._rel

    @staticmethod
    def is_moving():
        return Mouse._moving
