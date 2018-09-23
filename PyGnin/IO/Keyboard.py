from pygame.locals import *


class Keyboard(object):
    _keysUp = {}
    _keysDown = {}
    _keysHeld = {}

    @staticmethod
    def update(event):
        if event.type == KEYDOWN:
            if not Keyboard.is_held(event.key):
                Keyboard._keysDown[event.key] = True
            Keyboard._keysHeld[event.key] = True
            if event.key in Keyboard._keysUp:
                del Keyboard._keysUp[event.key]

        if event.type == KEYUP:
            Keyboard._keysUp[event.key] = True
            if event.key in Keyboard._keysDown:
                del Keyboard._keysDown[event.key]
            if event.key in Keyboard._keysHeld:
                del Keyboard._keysHeld[event.key]

    @staticmethod
    def is_up(key):
        if key in Keyboard._keysUp and Keyboard._keysUp[key]:
            del Keyboard._keysUp[key]
            return True
        return False

    @staticmethod
    def is_down(key):
        if key in Keyboard._keysDown and Keyboard._keysDown[key]:
            del Keyboard._keysDown[key]
            return True
        return False

    @staticmethod
    def is_held(key):
        if key in Keyboard._keysHeld and Keyboard._keysHeld[key]:
            return True
        return False
