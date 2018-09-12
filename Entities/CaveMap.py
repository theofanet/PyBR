from Entities.Rock import *
import pygame
import random
import json

from Helpers.AStar import a_star
from Sprites.Chest import Chest
from Sprites.Doors import Doors
from Sprites.Monster import Monster


PATHS_COLORS = [
    (241, 196, 15),
    (230, 126, 34),
    (231, 76, 60),
    (236, 240, 241),
    (149, 165, 166)
]


class CaveMap(object):
    def __init__(self, width=0, height=0):
        super().__init__()
        self.tile_size = 16
        self.width = width
        self.height = height
        self._size = (width * self.tile_size, height * self.tile_size)
        self._tiles = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self._mini_map = None
        self._objects = []
        self._start_position = Doors()
        self._end_position = Doors()
        self._monsters = []
        self._paths = []

    def init(self, steps=0, nb_monsters=0, place_start_end=False, mini_map=False, place_tiles=True):
        self._objects = []
        self._monsters = []
        self._paths = []
        self._mini_map = pygame.Surface(self._size)
        self._mini_map.fill((33, 33, 33))
        self._start_position.close()
        self._end_position.close()

        if place_tiles:
            for y in range(self.height):
                for x in range(self.width):
                    r = random.random()
                    if r < 0.45:
                        self._tiles[y][x] = 1
                    else:
                        self._tiles[y][x] = 0

        for _ in range(steps):
            self.generate_step()

        for _ in range(nb_monsters):
            self.add_monster()

        if place_start_end:
            self.place_start_end()

        if mini_map:
            self.generate_mini_map()

    def generate_step(self):
        death_limit = 4
        birth_limit = 4
        new_tiles = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                count = self.count_alive_neighbours(x, y)
                if self._tiles[y][x]:
                    new_tiles[y][x] = 1 if count >= death_limit else 0
                else:
                    new_tiles[y][x] = 1 if count > birth_limit else 0
        self._tiles = new_tiles

    def draw(self, surface=None, camera=None, mini_map=False, paths=False):
        if not self._tiles:
            return None
        if not surface:
            surface = App.get_display()

        if mini_map:
            surface.fill((33, 33, 33))
            rect = self._mini_map.get_rect()
            surface.blit(self._mini_map, rect)
        else:
            x_start = 0
            x_end = self.width
            y_start = 0
            y_end = self.height

            if camera:
                x_start = int(camera.position[0] / self.tile_size) - 1
                y_start = int(camera.position[1] / self.tile_size) - 1
                x_end = x_start + int(camera.viewSize[0] / self.tile_size) + 2
                y_end = y_start + int(camera.viewSize[1] / self.tile_size) + 2

            for y in range(y_start, y_end):
                if 0 <= y < len(self._tiles):
                    for x in range(x_start, x_end):
                        if 0 <= x < len(self._tiles[y]):
                            if self._tiles[y][x]:
                                self.draw_point(surface, x, y, (9, 132, 227), camera)

            for chest in self._objects:
                chest.draw(surface, camera)

            self._start_position.draw(surface, camera)

            self._end_position.draw(surface, camera)

            for monster in self._monsters:
                monster.draw(surface, camera)

            if paths:
                i = 0
                for path in self._paths:
                    for (x, y) in path:
                        self.draw_point(surface, x, y, PATHS_COLORS[i % 4], camera=camera)
                    i += 1

    def draw_point(self, surface, x, y, p_color=(0, 0, 0), camera=None):
        rect = pygame.Rect((self.tile_size * x), (self.tile_size * y), self.tile_size, self.tile_size)
        if camera:
            rect.x -= camera.get_position()[0]
            rect.y -= camera.get_position()[1]
        pygame.draw.rect(surface, p_color, rect)

    def generate_mini_map(self, paths=False):
        self._mini_map = pygame.Surface(self._size)
        self._mini_map.fill((33, 33, 33))
        self.draw(surface=self._mini_map, paths=paths)
        self._mini_map = pygame.transform.scale(self._mini_map, (
            App.get_screen_size()[0],
            App.get_screen_size()[1]
        ))

    def add_path(self, path, draw_mini_map=True):
        self._paths.append(path)
        if draw_mini_map:
            self.generate_mini_map(True)

    def update(self):
        for monster in self._monsters:
            monster.update()

    def generate_path(self):
        paths = []
        paths_found = [False, False, False]
        _start_pos = (0, 0)
        end_pos = (0, 0)

        i = 0
        while not paths_found[0]:
            print("SEARCHING FIRST PATH")
            #random.seed(self._seeds[i])
            _start_pos = self.get_random_position()
            start_pos = _start_pos
            end_pos = self.get_random_position()
            try:
                path = a_star(self._tiles, (start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]))
                if path:
                    print("FIRST PATH FOUND")
                    paths_found[0] = True
                    paths.extend(path)
            except IndexError:
                pass
            i += 1
            if i >= 20:
                i - 0

        i = 0
        while not paths_found[1]:
            print("SEARCHING SECOND PATH")
            #random.seed(self._seeds[i])
            start_pos = end_pos
            end_pos = self.get_random_position()
            try:
                path = a_star(self._tiles, (start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]))
                if path:
                    paths.extend(path)
                    paths_found[1] = True
                    print("SECOND PATH FOUND")
            except IndexError:
                pass
            i += 1
            if i >= 20:
                i - 0

        i = 0
        while not paths_found[2]:
            print("SEARCHING THIRD PATH")
            start_pos = end_pos
            end_pos = _start_pos
            try:
                path = a_star(self._tiles, (start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]))
                if path:
                    paths.extend(path)
                    print("THIRD PATH FOUND")
                    paths_found[2] = True
                else:
                    return False
            except IndexError:
                return False

        return paths

    def add_monster(self):
        paths = False
        while not paths:
            paths = self.generate_path()

        monster = Monster()
        monster.launch_path(paths, loop=True)
        self._monsters.append(monster)

        self.add_path(paths)

    def place_object(self, scene=None):
        object_limit = 5
        placed = False
        while not placed:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            count = self.count_alive_neighbours(x, y)
            if (x, y) not in self._objects and count < object_limit:
                chest = Chest()
                chest.set_position(self.tile_size * x, self.tile_size * y)
                self._objects.append(chest)
                if scene:
                    scene.add_sprites(chest)
                placed = True

    def place_start_end(self, mini_map=True):
        start_x, start_y = self.get_random_position()
        end_x, end_y = self.get_random_position()
        self._start_position.set_position(self.tile_size * start_x, self.tile_size * start_y)
        self._end_position.set_position(self.tile_size * end_x, self.tile_size * end_y)
        if mini_map:
            self.generate_mini_map(True)

    def get_random_position(self):
        object_limit = 2
        position = (0, 0)
        placed = False
        while not placed:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            count = self.count_alive_neighbours(x, y)
            if count < object_limit:
                position = (x, y)
                placed = True
        return position

    def count_alive_neighbours(self, x, y):
        count = 0
        i = -1
        while i < 2:
            j = -1
            while j < 2:
                n_x = x+i
                n_y = y+j
                if i == 0 and j == 0:
                    pass
                elif n_x < 0 or n_y < 0 or n_x >= self.width or n_y >= self.height:
                    count += 1
                elif self.width > n_x >= 0 and self.height > n_y >= 0 and self._tiles[n_y][n_x]:
                    count += 1
                j += 1
            i += 1
        return count

    def nb_objects(self):
        return len(self._objects)

    def nb_monsters(self):
        return len(self._monsters)

    def get_objects(self):
        return self._objects

    def get_size(self):
        return self._size

    def get_tiles(self):
        return self._tiles

    def get_start_position(self):
        return \
            int(self._start_position.get_position()[0] / self.tile_size), \
            int(self._start_position.get_position()[1] / self.tile_size)

    def get_end_position(self):
        return \
            int(self._end_position.get_position()[0] / self.tile_size), \
            int(self._end_position.get_position()[1] / self.tile_size)

    def get_start_pos(self):
        return self._start_position

    def get_end_pos(self):
        return self._end_position

    def destroy_tile(self, x, y):
        self._tiles[y][x] = 0
        self.generate_mini_map()

    def check_chest_collision(self, player):
        player_bbox = player.get_bbox()
        colliding_chest = None
        chests_openable = []
        for chest in self._objects:
            if chest.check_collision(player_bbox, open_bbox=True):
                chests_openable.append(chest)
                if chest.check_collision(player_bbox):
                    colliding_chest = chest
        return colliding_chest, chests_openable

    def check_wall_collision(self, player, camera=None):
        x_start = 0
        x_end = self.width
        y_start = 0
        y_end = self.height

        if camera:
            view_offset = 10
            x_start = int(camera.position[0] / self.tile_size) - view_offset
            y_start = int(camera.position[1] / self.tile_size) - view_offset
            x_end = x_start + int(camera.viewSize[0] / self.tile_size) + view_offset
            y_end = y_start + int(camera.viewSize[1] / self.tile_size) + view_offset

        player_bbox = player.get_bbox()
        for y in range(y_start, y_end):
            if 0 <= y < len(self._tiles):
                for x in range(x_start, x_end):
                    if 0 <= x < len(self._tiles[y]):
                        if self._tiles[y][x]:
                            rect = pygame.Rect((self.tile_size*x), (self.tile_size*y), self.tile_size, self.tile_size)
                            if player_bbox.colliderect(rect):
                                return x, y

    def export(self, filename):
        data = {
            "size": self._size,
            "start": self._start_position.get_position(),
            "end": self._end_position.get_position(),
            "tiles": self._tiles,
            "chests": [],
            "monsters": [],
            "paths": self._paths
        }

        for chests in self._objects:
            data["chests"].append(chests.to_json())
        for monster in self._monsters:
            data["monsters"].append(monster.to_json())

        with open("Maps/" + filename, 'w+') as outfile:
            json.dump(data, outfile)

    def import_json(self, filename):
        self.init()
        with open("Maps/" + filename) as f:
            data = json.load(f)
        if "start" in data:
            self._start_position.set_position(data["start"][0], data["start"][1])
        if "end" in data:
            self._end_position.set_position(data["end"][0], data["end"][1])
        if "tiles" in data:
            self._tiles = data["tiles"]
        if "chests" in data:
            for c in data["chests"]:
                chest = Chest(json_data=c)
                self._objects.append(chest)
        if "monsters" in data:
            for m in data["monsters"]:
                monster = Monster(json_data=m)
                self._monsters.append(monster)
        if "paths" in data:
            self._paths = data["paths"]
        self.generate_mini_map(True)