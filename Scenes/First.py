from PyGnin import *
from Entities import Map
import Sprites
import time
from PyGnin.Render import Font


class FirstScene(Game.Scene):
    def __init__(self):
        super().__init__()
        self._showMap = False
        self._font = Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf")
        self._map = Map(200, 200, int(time.time()), 2.2, 0.2)
        self._player = Sprites.Player()
        self.add_sprites(self._player)
        self._player.set_play_size(self._map.get_size())
        self._camera = Render.Camera((200, 200), speed=self._player.get_speed())

    def _load_resources(self):
        App.show_cursor(False)
        self._player.set_aim_color(list(map(int, Registry.registered("config").get("aim", "color").split(","))))

    def update(self):
        if IO.Keyboard.is_down(K_m):
            self._showMap = not self._showMap
        elif IO.Keyboard.is_down(K_ESCAPE):
            App.set_active_scene("menu")

        if not self._showMap:
            super().update()
            self._camera.update(self._player.get_position(), self._player.get_direction(), self._map.get_size())

    def draw(self):
        self._map.draw(camera=self._camera, mini_map=self._showMap, player_position=self._player.get_position())
        if not self._showMap:
            super().draw_sprites(self._camera)
            # self._font.draw_text("Hello World")
            # self._font.draw_text("Hello World", (0, 50), (255, 0, 0))
