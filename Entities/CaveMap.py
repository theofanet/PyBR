from Entities.Rock import *
import pygame
import random


class CaveMap(object):
    def __init__(self, width=0, height=0):
        super().__init__()
        self.tile_size = 16
        self.width = width
        self.height = height
        self._size = (width * self.tile_size, height * self.tile_size)
        self._tiles = [[False for _ in range(self.height)] for _ in range(self.width)]
        self._mini_map = None
        self._objects = []
        self._start_position = (0, 0)
        self._end_position = (0, 0)

    def init(self, steps=0):
        self._objects = []
        self._mini_map = pygame.Surface(self._size)
        self._mini_map.fill((33, 33, 33))

        for x in range(self.width):
            for y in range(self.height):
                r = random.random()
                if r < 0.45:
                    self._tiles[x][y] = True
                else:
                    self._tiles[x][y] = False

        for _ in range(steps):
            self.generate_step()

        self.place_start_end()

    def generate_step(self):
        death_limit = 4
        birth_limit = 4
        new_tiles = [[False for _ in range(self.height)] for _ in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                count = self.count_alive_neighbours(x, y)
                if self._tiles[x][y]:
                    new_tiles[x][y] = count >= death_limit
                else:
                    new_tiles[x][y] = count > birth_limit
        self._tiles = new_tiles

    def draw(self, surface=None, camera=None, mini_map=False):
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

            for x in range(x_start, x_end):
                if 0 <= x < len(self._tiles):
                    for y in range(y_start, y_end):
                        if 0 <= y < len(self._tiles[x]):
                            if self._tiles[x][y]:
                                self.draw_point(surface, x, y, (9, 132, 227), camera)

            for (x, y) in self._objects:
                self.draw_point(surface, x, y, (253, 203, 110), camera)

            x, y = self._start_position
            self.draw_point(surface, x, y, (68, 189, 50), camera)

            x, y = self._end_position
            self.draw_point(surface, x, y, (214, 48, 49), camera)

    def draw_point(self, surface, x, y, p_color=(0, 0, 0), camera=None):
        rect = pygame.Rect((self.tile_size * x), (self.tile_size * y), self.tile_size, self.tile_size)
        if camera:
            rect.x -= camera.get_position()[0]
            rect.y -= camera.get_position()[1]
        pygame.draw.rect(surface, p_color, rect)

    def generate_mini_map(self):
        self._mini_map = pygame.Surface(self._size)
        self._mini_map.fill((33, 33, 33))
        self.draw(surface=self._mini_map)
        self._mini_map = pygame.transform.scale(self._mini_map, (
            App.get_screen_size()[0],
            App.get_screen_size()[1]
        ))

    def update(self):
        pass

    def place_object(self):
        object_limit = 5
        placed = False
        while not placed:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            count = self.count_alive_neighbours(x, y)
            if (x, y) not in self._objects and count < object_limit:
                self._objects.append((x, y))
                placed = True

    def place_start_end(self):
        self._start_position = self.get_random_position()
        self._end_position = self.get_random_position()

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
                elif self.width > n_x >= 0 and self.height > n_y >= 0 and self._tiles[n_x][n_y]:
                    count += 1
                j += 1
            i += 1
        return count

    def nb_objects(self):
        return len(self._objects)

    def get_size(self):
        return self._size

    def get_start_pos(self):
        return self._start_position

    def destroy_tile(self, x, y):
        self._tiles[x][y] = False
        self.generate_mini_map()

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
        for x in range(x_start, x_end):
            if 0 <= x < len(self._tiles):
                for y in range(y_start, y_end):
                    if 0 <= y < len(self._tiles[x]):
                        if self._tiles[x][y]:
                            rect = pygame.Rect((self.tile_size*x), (self.tile_size*y), self.tile_size, self.tile_size)
                            if player_bbox.colliderect(rect):
                                return x, y
