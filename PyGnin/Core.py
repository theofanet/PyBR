import sys
import atexit

from .IO import *
import PyGnin.Gui as Gui


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
    _time = 0
    _gui_screen = None

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
        Debug.init(font_size=16)
        App._gui_screen = Gui.surface.Screen(size, flags, display=App._window)
        App._font = pygame.font.SysFont("arial", 26)
        atexit.register(App.exit)

    @staticmethod
    def get_display():
        return App._window

    @staticmethod
    def get_screen_size():
        return App._screenSize

    @staticmethod
    def show_cursor(visible):
        pygame.mouse.set_visible(visible)

    @staticmethod
    def set_active_scene(scene):
        if App._activeScene:
            App._scenes[App._activeScene].close_scene()
        if scene in App._scenes:
            App._activeScene = scene
            App._scenes[App._activeScene].activate()

    @staticmethod
    def get_active_scene():
        if App._activeScene:
            return App._scenes[App._activeScene]

    @staticmethod
    def load_scene(key, scene):
        App._scenes[key] = scene

    @staticmethod
    def exit():
        if App._activeScene:
            App._scenes[App._activeScene].close_scene()
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
    def get_time():
        return App._time

    @staticmethod
    def show_fps(show=True):
        App._showFps = show

    @staticmethod
    def get_background_color():
        return App._backgroundColor

    @staticmethod
    def draw_loading(message="Loading ...", font=None, pos=None, col=(255, 255, 255), back=(0, 0, 0)):
        if not pos:
            pos = (20, App._screenSize[1] - 50)
        App._window.fill(back)
        if not font:
            txt = App._font.render(message, True, col)
            App._window.blit(txt, pos)
        else:
            font.draw_text(message, pos, col, App._window)
        pygame.display.update()

    @staticmethod
    def run():
        while True:
            for event in pygame.event.get():
                Gui.event(event)
                Keyboard.update(event)
                Mouse.update(event)
                if event.type == QUIT:
                    App.exit()

            pygame.time.wait(0)

            App._window.fill(App._backgroundColor)

            # Updating and drawing active scene
            if App._activeScene:
                App._scenes[App._activeScene].draw()
                App._scenes[App._activeScene].update()

            Debug.draw(App._window)

            pygame.display.update()

            App._time = App._clock.tick(App._FPS)
            if App._showFps:
                Debug.log("FPS : {0:.2f}", App._clock.get_fps())
                # App.set_title("{0} - {1} FPS".format(App._title, round(App._clock.get_fps(), 2)))
