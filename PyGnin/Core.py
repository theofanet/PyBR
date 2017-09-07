import pygame
import sys
import atexit

from .IO import *


class App(object):
    _FPS = 60
    _activeScene = None
    _scenes = {}
    _window = None
    _screenSize = (0, 0)
    _backgroundColor = (0, 0, 0)
    _clock = None
    _showFps = False
    _title = ""
    _font = None

    @staticmethod
    def init(size=(0, 0), background=(0, 0, 0), mouse_visible=True, title="Gnin App", fps=60, show_fps=False, fullscreen=False):
        App._screenSize = size
        App._backgroundColor = background
        pygame.init()
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        if fullscreen:
            flags = flags | pygame.FULLSCREEN
        App._window = pygame.display.set_mode(App._screenSize, flags)
        App._title = title
        pygame.display.set_caption(App._title)
        if not mouse_visible:
            pygame.mouse.set_visible(0)
        App._clock = pygame.time.Clock()
        App._FPS = fps
        App._showFps = show_fps
        App._font = pygame.font.SysFont("monospace", 15)
        atexit.register(App.exit)

    @staticmethod
    def get_display():
        return App._window

    @staticmethod
    def get_screen_size():
        return App._screenSize

    @staticmethod
    def set_active_scene(scene):
        if scene in App._scenes:
            App._activeScene = scene
            App._scenes[App._activeScene].activate()

    @staticmethod
    def load_scene(key, scene):
        App._scenes[key] = scene

    @staticmethod
    def exit():
        if App._window:
            App._window = None
            pygame.quit()
            sys.exit()

    @staticmethod
    def set_title(title):
        pygame.display.set_caption(title)

    @staticmethod
    def get_clock():
        return App._clock

    @staticmethod
    def run():
        while True:
            for event in pygame.event.get():
                Keyboard.update(event)
                Mouse.update(event)
                if event.type == QUIT or Keyboard.is_down(K_ESCAPE):
                    App.exit()

            pygame.time.wait(0)

            App._window.fill(App._backgroundColor)

            # Updating and drawing active scene
            if App._activeScene:
                App._scenes[App._activeScene].update()
                App._scenes[App._activeScene].draw()

            pygame.display.update()

            label = App._font.render("Some text!", 1, (255, 255, 0))
            App._window.blit(label, (100, 100))

            App._clock.tick(App._FPS)
            if App._showFps:
                App.set_title("{0} - {1} FPS".format(App._title, round(App._clock.get_fps(), 2)))
