from PyGnin import *
from Entities import Map
import Sprites
import time
from PyGnin.Render import Font
import Scenes


class FirstScene(Game.Scene):
    def __init__(self):
        super().__init__()
        self._showMap = False
        self._font = Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf")
        self._map = Map(200, 200)
        self._player = Sprites.Player()
        self.add_sprites(self._player)
        self._player.set_play_size(self._map.get_size())
        self._camera = Render.Camera((200, 200), speed=self._player.get_speed())
        self._menu_subScene = Scenes.Sub.SoloMenu()
        self._is_menu_shown = False

    def _load_resources(self):
        App.show_cursor(False)
        self._map.generate(
            int(time.time()),
            Registry.registered("config").getfloat("map", "frequency"),
            Registry.registered("config").getfloat("map", "water_level")
        )
        self._player.set_aim_color(list(map(int, Registry.registered("config").get("aim", "color").split(","))))
        self._menu_subScene.initiate(self)
        self._menu_subScene.resumeButton.on_click = self.resume_game

    def update(self):
        if not self._is_menu_shown:
            if IO.Keyboard.is_down(K_m):
                self._showMap = not self._showMap
            elif IO.Keyboard.is_down(K_ESCAPE):
                self._menu_subScene.activate()
                self._is_menu_shown = True

            if not self._showMap:
                x, y = self._player.get_position()
                super().update()
                self._camera.update(self._player.get_position(), self._player.get_direction(), self._map.get_size())
                if self._map.check_water_collision(self._player, self._camera):
                    self._player.set_position(x, y)
        else:
            self._menu_subScene.update()

    def draw(self):
        if self._is_menu_shown:
            self._menu_subScene.draw()
        else:
            self._map.draw(camera=self._camera, mini_map=self._showMap, player_position=self._player.get_position())
            if not self._showMap:
                super().draw_sprites(self._camera)
                self._map.draw_foreground(camera=self._camera)

    def resume_game(self):
        self._menu_subScene.close()
        self._is_menu_shown = False
        if self._menu_subScene.settingsSubMenu.reloadMapSwitch.state:
            self._menu_subScene.settingsSubMenu.reloadMapSwitch.config(state=False)
            self._map.generate(
                int(time.time()),
                Registry.registered("config").getfloat("map", "frequency"),
                Registry.registered("config").getfloat("map", "water_level")
            )
