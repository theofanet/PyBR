from PyGnin import *


class Menu(Game.Scene):
    def __init__(self):
        super().__init__()
        self._settingsButton = Gui.Button(label="Settings", pos=(App.get_screen_size()[0] / 2 - 55, 250))
        self._settingsButton.on_click = Menu.show_settings
        self._resumeButton = Gui.Button(label="Resume", pos=(App.get_screen_size()[0] / 2 - 55, 200))
        self._resumeButton.on_click = Menu.resume_game
        self._quitButton = Gui.Button(label="Quit", pos=(App.get_screen_size()[0] / 2 - 55, 300))
        self._quitButton.on_click = Menu.quit_game

    def _load_resources(self):
        App.show_cursor(True)
        self._resumeButton.add()
        self._quitButton.add()
        self._settingsButton.add()

    def close_scene(self):
        self._resumeButton.remove(False)
        self._quitButton.remove(False)
        self._settingsButton.remove(False)

    def draw(self):
        App.get_display().fill((0, 0, 0))
        Gui.update(App.get_time())
        super().draw()

    @staticmethod
    def show_settings():
        App.set_active_scene("settings")

    @staticmethod
    def resume_game():
        App.set_active_scene("main")

    @staticmethod
    def quit_game():
        App.exit()
