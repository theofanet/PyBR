from PyGnin import *
import Sprites
from PyGnin.Render import Font

from Entities.CaveMap import CaveMap


INIT_MODE = 0
LOOT_MODE = 1
EXTRACT_MODE = 2
GAME_OVER_MODE = 6

LOOT_TIME = 180
EXTRACT_TIME = 30

class CaveScene(Game.Scene):
    def __init__(self):
        super().__init__()
        self._map = CaveMap(200, 150)
        self.update_step = 15
        self.nb_objects = 25
        self._init_done = False
        self._game_mode = INIT_MODE
        self._show_mini_map = True
        self.current_step = 0
        self._player = Sprites.Player()
        self.add_sprites(self._player)
        self._player.set_play_size(self._map.get_size())
        self._camera = Render.Camera((200, 200), speed=self._player.get_speed(), map_size=self._map.get_size())
        self._time = 0
        self._font = Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf")
        self._alert_color = False

    def _load_resources(self):
        App.show_cursor(True)
        self.current_step = 0
        self._map.init()

    def get_time_humanized(self, rest):
        conv = (31536000, 2592000, 86400, 3600, 60, 1)
        result = [0, 0, 0, 0, 0, 0]
        i = 0
        while rest > 0:
            result[i], rest = divmod(rest, conv[i])
            i += 1
        return result

    def update(self):
        if not self._init_done:
            if self.current_step < self.update_step:
                self._map.generate_step()
                self._map.generate_mini_map()
                self.current_step += 1
            elif self._map.nb_objects() < self.nb_objects:
                self._map.place_object()
                self._map.generate_mini_map()
            else:
                self._map.place_start_end()
                self._map.generate_mini_map()
                pos = self._map.get_start_pos()
                self._player.set_position(pos[0]*16-self._player.rect.w/3, pos[1]*16-self._player.rect.h/2)
                self._camera.center_camera(pos[0]*16, pos[1]*16)
                self._init_done = True
                self._game_mode = LOOT_MODE
        else:
            self._time += App.get_time()

            if self._game_mode == LOOT_MODE:
                t = LOOT_TIME - EXTRACT_TIME - self._time / 1000
                if t < 0:
                    self._time = 0
                    self._game_mode = EXTRACT_MODE
            elif self._game_mode == EXTRACT_MODE:
                t = EXTRACT_TIME - self._time / 1000
                if t < 0:
                    self._time = 0
                    self._game_mode = GAME_OVER_MODE

            if not self._show_mini_map and not self._game_mode == GAME_OVER_MODE:
                x, y = self._player.get_position()
                super().update()
                self._camera.update(self._player.get_position(), self._player.get_direction(), self._map.get_size())
                if self._map.check_wall_collision(self._player, self._camera):
                    self._player.set_position(x, y)

                for bullet in self._player.get_bullets():
                    pos = self._map.check_wall_collision(bullet, self._camera)
                    if pos:
                        bullet.destroy()
                        self._map.destroy_tile(pos[0], pos[1])

            if IO.Keyboard.is_down(K_TAB):
                self._show_mini_map = not self._show_mini_map

    def draw(self):
        self._map.draw(camera=self._camera, mini_map=self._show_mini_map)
        if not self._show_mini_map:
            self._player.draw(App.get_display(), camera=self._camera)

        if self._game_mode == LOOT_MODE:
            t = LOOT_TIME - self._time / 1000
            self._font.draw_text("Loot time : %02d:%02d" % (int(t/60), int(t%60)), color=(251, 197, 49), position=(20, 20))
        elif self._game_mode == EXTRACT_MODE:
            t = EXTRACT_TIME - self._time / 1000
            if self._time % 10 == 0:
                self._alert_color = not self._alert_color
            c = (231, 76, 60)
            if not self._alert_color:
                c = (194, 54, 22)
            self._font.draw_text("EXTRACT : %02d:%02d" % (int(t/60), int(t%60)), color=c, position=(20, 20))
        elif self._game_mode == GAME_OVER_MODE:
            self._font.draw_text("GAME OVER", color=(194, 54, 22), position=(20, 20))
