from PyGnin import *
import Sprites
from PyGnin.Render import Font
from Entities.CaveMap import CaveMap


COLORS = {
    "butternut": (255, 218, 121),
    "red_toggle_1": (231, 76, 60),
    "red_toggle_2": (194, 54, 22),
    "green": (68, 189, 50)
}

WAITING_MODE = 0
INIT_MODE = 1
LOOT_MODE = 2
EXTRACT_MODE = 3
GAME_END_MODE = 4
GAME_OVER_MODE = 6

LOOT_TIME = 180
EXTRACT_TIME = 30


class CaveScene(Game.Scene):
    def __init__(self):
        super().__init__()
        self._map = CaveMap(200, 150)
        self.update_step = 15
        self.nb_objects = 25
        self.nb_monsters = 4
        self._init_done = False
        self._game_mode = WAITING_MODE
        self._show_mini_map = True
        self.current_step = 0
        self._player = Sprites.Player()
        self._player.set_play_size(self._map.get_size())
        self._camera = Render.Camera((200, 200), speed=self._player.get_speed(), map_size=self._map.get_size())
        self._time = 0
        self._global_time = 0
        self._font = Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf")
        self._title_font = Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf", size=70)
        self._alert_color = False
        self._opened_chests = []
        self._points = 0
        self.add_sprites(self._player)
        self.add_sprites(self._map.get_start_pos())
        self.add_sprites(self._map.get_end_pos())

        config = Registry.registered("config")
        screen = config.get("window", "size").split(",")
        self.SCREEN = [
            int(screen[0]),
            int(screen[1])
        ]

    def _load_resources(self):
        App.show_cursor(True)
        self.current_step = 0
        self._points = 0
        self._map.init(mini_map=True)

    def load_export(self):
        self.current_step = 0
        self._points = 0
        self._time = 0
        self._global_time = 0
        self._map.import_json("map-export.json")
        self._game_mode = LOOT_MODE
        start_door = self._map.get_start_pos()
        pos = start_door.get_position()
        start_door.open()
        self._player.set_position(pos[0]+start_door.get_frame_rect().w/3, pos[1]+start_door.get_frame_rect().h/3)
        self._camera.center_camera(pos[0], pos[1])
        self._init_done = True

    def update(self):
        self._global_time += App.get_time()

        if self._game_mode > WAITING_MODE:
            if not self._init_done:
                if self.current_step < self.update_step:
                    self._title_font.draw_text(
                        "MAP STEP %s" % self.current_step,
                        position=(self.SCREEN[0] / 2 - 220, self.SCREEN[1] / 2 - 50),
                        color=COLORS["butternut"],
                        update_display=True
                    )
                    self._map.generate_step()
                    self._map.generate_mini_map()
                    self.current_step += 1
                elif self._map.nb_objects() < self.nb_objects:
                    self._title_font.draw_text(
                        "ADDING CHEST %s" % (self._map.nb_objects() + 1),
                        position=(self.SCREEN[0] / 2 - 250, self.SCREEN[1] / 2 - 50),
                        color=COLORS["butternut"],
                        update_display=True
                    )
                    self._map.place_object(self)
                    self._map.generate_mini_map()
                elif self._map.nb_monsters() < self.nb_monsters:
                    self._title_font.draw_text(
                        "ADDING BAD GUY %s" % (self._map.nb_monsters() + 1),
                        position=(self.SCREEN[0] / 2 - 300, self.SCREEN[1] / 2 - 50),
                        color=COLORS["butternut"],
                        update_display=True
                    )
                    self._map.add_monster()
                else:
                    self._title_font.draw_text(
                        "PLACING PLAYER",
                        position=(self.SCREEN[0] / 2 - 220, self.SCREEN[1] / 2 - 50),
                        color=COLORS["butternut"],
                        update_display=True
                    )
                    self._map.place_start_end()
                    start_door = self._map.get_start_pos()
                    pos = start_door.get_position()
                    start_door.open()
                    self._player.set_position(pos[0]+start_door.get_frame_rect().w/3, pos[1]+start_door.get_frame_rect().h/3)
                    self._camera.center_camera(pos[0], pos[1])
                    self._init_done = True
                    self._game_mode = LOOT_MODE
            else:
                if IO.Keyboard.is_down(K_F1):
                    self._map.export("map-export.json")
                elif IO.Keyboard.is_down(K_F2):
                    self.load_export()

                if self._game_mode != GAME_OVER_MODE and self._game_mode != GAME_END_MODE:
                    self._time += App.get_time()

                    if self._game_mode == LOOT_MODE:
                        t = LOOT_TIME - EXTRACT_TIME - self._time / 1000
                        if t < 0:
                            self._time = 0
                            self._game_mode = EXTRACT_MODE
                            self._map.get_end_pos().open()
                    elif self._game_mode == EXTRACT_MODE:
                        t = EXTRACT_TIME - self._time / 1000
                        if t < 0:
                            self._time = 0
                            self._game_mode = GAME_OVER_MODE

                    if not self._show_mini_map:
                        x, y = self._player.get_position()
                        player_bbox = self._player.get_bbox()
                        super().update()
                        self._map.update()
                        self._camera.update(self._player.get_position(), self._player.get_direction(), self._map.get_size())
                        # wall collisions
                        if self._map.check_wall_collision(self._player, self._camera):
                            self._player.set_position(x, y)
                        # doors collisions
                        # chests collisions
                        chest, chests_openable = self._map.check_chest_collision(self._player)
                        if chest is not None:
                            self._player.set_position(x, y)
                        if self._game_mode == LOOT_MODE or self._game_mode == EXTRACT_MODE:
                            if IO.Keyboard.is_down(K_SPACE):
                                if len(chests_openable):
                                    for chest in chests_openable:
                                        chest.open()
                                        self._opened_chests.append(chest)
                                    self._map.generate_mini_map()
                            if self._game_mode == EXTRACT_MODE:
                                if self._map.get_end_pos().is_open() \
                                        and self._map.get_end_pos().check_collision(player_bbox, True):
                                    self._game_mode = GAME_END_MODE

                        for chest in self._opened_chests:
                            pts = chest.check_gem_collisions(player_bbox)
                            if pts:
                                self._points += pts

                        for bullet in self._player.get_bullets():
                            pos = self._map.check_wall_collision(bullet, self._camera)
                            if pos:
                                bullet.destroy()
                                self._map.destroy_tile(pos[0], pos[1])

                    if IO.Keyboard.is_down(K_TAB):
                        self._show_mini_map = not self._show_mini_map

                    if IO.Keyboard.is_down(K_h):
                        self._map.get_start_pos().open()
        elif self._game_mode == WAITING_MODE:
            if IO.Keyboard.is_down(K_RETURN):
                self._game_mode = INIT_MODE

    def draw(self):
        self._map.draw(camera=self._camera, mini_map=self._show_mini_map)

        if self._game_mode == WAITING_MODE:
            self._title_font.draw_text("CAVE GAME", position=(self.SCREEN[0] / 2 - 180, 20), color=COLORS["butternut"])
            if self._global_time % 10 == 0:
                self._alert_color = not self._alert_color
            c = COLORS["red_toggle_1"]
            if not self._alert_color:
                c = COLORS["red_toggle_2"]
            self._title_font.draw_text("LAUNCH GAME", position=(self.SCREEN[0] / 2 - 220, self.SCREEN[1] / 2 - 50), color=c)
        else:
            if not self._show_mini_map:
                self._player.draw(App.get_display(), camera=self._camera)

            if self._game_mode != INIT_MODE:
                c = COLORS["butternut"]
                if self._game_mode == GAME_END_MODE:
                    c = COLORS["green"]
                elif self._game_mode == GAME_OVER_MODE:
                    c = COLORS["red_toggle_2"]
                self._font.draw_text("POINTS : %i" % self._points, color=c, position=(20, 60))

                if self._game_mode == LOOT_MODE:
                    t = LOOT_TIME - self._time / 1000
                    self._font.draw_text("Loot time : %02d:%02d" % (int(t/60), int(t%60)), color=c, position=(20, 20))
                elif self._game_mode == EXTRACT_MODE:
                    t = EXTRACT_TIME - self._time / 1000
                    if self._time % 10 == 0:
                        self._alert_color = not self._alert_color
                    c = COLORS["red_toggle_1"]
                    if not self._alert_color:
                        c = COLORS["red_toggle_2"]
                    self._font.draw_text("EXTRACT : %02d:%02d" % (int(t/60), int(t%60)), color=c, position=(20, 20))
                elif self._game_mode == GAME_OVER_MODE:
                    self._font.draw_text("GAME OVER", color=c, position=(20, 20))
                elif self._game_mode == GAME_END_MODE:
                    t = EXTRACT_TIME - self._time / 1000
                    self._font.draw_text("Remaining time : %02d:%02d" % (int(t/60), int(t%60)), color=c, position=(20, 20))
                    self._font.draw_text("EXTRACTED ! WELL DONE !", color=c, position=(20, 100))