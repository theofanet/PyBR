from PyGnin import *
from PyGnin.Render import Font

from Entities.CaveMap import CaveMap
from Helpers.AStar import a_star


class AStarScene(Game.Scene):
    def __init__(self):
        super().__init__()
        self._map = CaveMap(200, 150)
        self.update_step = 15
        self.nb_objects = 25
        self._init_done = False
        self._show_mini_map = True
        self.current_step = 0
        self._camera = Render.Camera((200, 200), map_size=self._map.get_size())
        self._time = 0
        self._font = Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf")
        self.add_sprites(self._map.get_start_pos())
        self.add_sprites(self._map.get_end_pos())
        self._paths = []

    def _load_resources(self):
        App.show_cursor(True)
        self.current_step = 0
        self._points = 0
        self._map.init()

    def update(self):
        if not self._init_done:
            if self.current_step < self.update_step:
                self._map.generate_step()
                self._map.generate_mini_map()
                self.current_step += 1
            elif self._map.nb_objects() < self.nb_objects:
                self._map.place_object(self)
                self._map.generate_mini_map()
            else:
                self._map.place_start_end()
                start_door = self._map.get_start_pos()
                start_pos = start_door.get_position()
                self._camera.center_camera(start_pos[0], start_pos[1])
                self._init_done = True
                self._map.generate_mini_map()
                print("SEARCHING PATH")
                _start_pos = self._map.get_random_position()
                start_pos = _start_pos
                end_pos = self._map.get_random_position()
                print(start_pos)
                print(end_pos)
                self._paths = a_star(self._map.get_tiles(), (start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]))
                if self._paths:
                    print("PATH FOUND")
                    print("SEARCHING PATH")
                    start_pos = end_pos
                    end_pos = self._map.get_random_position()
                    paths = a_star(self._map.get_tiles(), (start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]))
                    if paths:
                        self._paths.extend(paths)
                        print("PATH FOUND")
                        print("SEARCHING PATH")
                        start_pos = end_pos
                        end_pos = _start_pos
                        paths = a_star(self._map.get_tiles(), (start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]))
                        if paths:
                            self._paths.extend(paths)
                            print("PATH FOUND")
                            self._map.draw_path_to_mini_map(self._paths)
                        else:
                            print("LAST NOT FOUND")
                    else:
                        print("SECOND NOT FOUND")
                else:
                    print("FIRST NOT FOUND")
        else:
            if IO.Keyboard.is_down(K_TAB):
                self._show_mini_map = not self._show_mini_map

    def draw(self):
        self._map.draw(camera=self._camera, mini_map=self._show_mini_map, path=self._paths)