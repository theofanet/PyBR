from PyGnin import *
from Entities import Map
import Sprites
import time
from PyGnin.Render import Font


class GameSubScene(Game.SubScene):
    def __init__(self):
        super().__init__()
        self._showMap = False
        self._font = None
        self._map = None
        self.player = None
        self._camera = None
        self._otherPlayers = {}

    def _initiate_data(self, **kargs):
        self._showMap = False
        self._font = Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf")
        self._map = Map(200, 200, int(time.time()), 2.2, 0.2)
        self.player = Sprites.Player()
        self.player.set_play_size(self._map.get_size())
        self._camera = Render.Camera((200, 200), speed=self.player.get_speed())

    def add_player(self, token):
        self._otherPlayers[token] = Sprites.Player(active=False)

    def activate(self):
        App.show_cursor(False)
        self.player.set_aim_color(list(map(int, Registry.registered("config").get("aim", "color").split(","))))
        self._scene.add_sprites(self.player)
        for token, sprite in self._otherPlayers.items():
            self._scene.add_sprites(sprite)

    def update(self):
        if IO.Keyboard.is_down(K_m):
            self._showMap = not self._showMap
        elif IO.Keyboard.is_down(K_ESCAPE):
            App.set_active_scene("menu")

        if not self._showMap:
            self._camera.update(self.player.get_position(), self.player.get_direction(), self._map.get_size())

        return not self._showMap

    def draw(self):
        self._map.draw(camera=self._camera, mini_map=self._showMap, player_position=self.player.get_position())
        if not self._showMap:
            self._scene.draw_sprites(self._camera)

    def get_camera(self):
        return self._camera

    def set_players(self, players_data, active_token):
        for data in players_data:
            if "token" in data and data["token"] != active_token:
                self.add_player(data["token"])

    def update_players(self, players_data):
        for data in players_data:
            if "token" in data and data["token"] in self._otherPlayers.keys():
                if "position" in data:
                    print(data)
                    self._otherPlayers[data["token"]].set_position(data["position"][0], data["position"][1])

    def update_player(self, token, data):
        if token in self._otherPlayers.keys():
            if "position" in data:
                self._otherPlayers[token].set_position(data["position"][0], data["position"][1])

    def close(self):
        self._scene.remove_sprites(self.player)
        for token, sprite in self._otherPlayers.items():
            self._scene.remove_sprites(sprite)
