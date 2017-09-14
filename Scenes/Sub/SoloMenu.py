from PyGnin import *
import Scenes


class SoloMenu(Game.SubScene):
    def __init__(self):
        super().__init__()
        self._settingsButton = Gui.Button(label="Settings", pos=(App.get_screen_size()[0] / 2 - 55, 250))
        self._settingsButton.on_click = self.show_settings
        self.resumeButton = Gui.Button(label="Resume", pos=(App.get_screen_size()[0] / 2 - 55, 200))
        self._quitButton = Gui.Button(label="Quit", pos=(App.get_screen_size()[0] / 2 - 55, 300))
        self._quitButton.on_click = SoloMenu.quit_game
        self.settingsSubMenu = Scenes.Sub.SoloSettings()
        self._mapReloadLabel = Gui.Label(text="* Map will be reload", pos=(App.get_screen_size()[0] / 2 + 70, 215))
        self._show_settings = False

    def initiate(self, scene, **kargs):
        super().initiate(scene, **kargs)
        self.settingsSubMenu.initiate(self)
        self.settingsSubMenu.returnButton.on_click = self.return_menu

    def activate(self):
        App.show_cursor(True)
        self.show_gui()

    def show_gui(self):
        self.resumeButton.add()
        self._quitButton.add()
        self._settingsButton.add()
        if self.settingsSubMenu.reloadMapSwitch.state:
            self._mapReloadLabel.add()

    def remove_gui(self):
        self.resumeButton.remove(False)
        self._quitButton.remove(False)
        self._settingsButton.remove(False)
        self._mapReloadLabel.remove(False)

    def close(self):
        self.remove_gui()
        self.settingsSubMenu.close()
        App.show_cursor(False)

    def draw(self, camera=None, screen=None):
        if self._show_settings:
            self.settingsSubMenu.draw(camera, screen)
        else:
            if not screen:
                screen = App.get_display()
            screen.fill((0, 0, 0))
            Gui.update(App.get_time())
            super().draw(camera, screen)

    def show_settings(self):
        self.remove_gui()
        self._show_settings = True
        self.settingsSubMenu.activate()

    @staticmethod
    def quit_game():
        App.exit()

    def return_menu(self):
        self.show_gui()
        self.settingsSubMenu.remove_gui()
        self._show_settings = False
