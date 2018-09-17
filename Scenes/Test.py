from PyGnin import *
from random import randint
import pygame

LOCKERS_NB = 30
LOCKERS_LENGHT = 10
LOCKERS_WIDTH = 40

LOCKER_UP = 0
LOCKER_MID = 1
LOCKER_DOWN = 2

SCREEN_W = 600
SCREEN_L = 800
SCREEN_CENTER_X = SCREEN_L / 2
SCREEN_CENTER_Y = SCREEN_W / 2


# grid entity.
class Grid:

    def __init__(self):
        self.l = LOCKERS_NB * LOCKERS_LENGHT * 2
        self.w = LOCKERS_WIDTH * 2

        self.y = SCREEN_CENTER_Y - (self.w / 2)
        self.x = SCREEN_CENTER_X - (self.l / 2)

        self.start_pos = SCREEN_CENTER_X + (self.l / 2)
        self.rect = None

        self.lockers_list = list()

    # init a list of lockers, depend of LOCKERS_NB.
    def init_lockers(self, nb_lockers: int):
        locker_modifier = LOCKERS_LENGHT * 1.5
        selector_modifier = LOCKERS_LENGHT * 1.7

        for i in range(nb_lockers):
            locker = Locker()
            locker_pos_y = SCREEN_CENTER_Y - (locker.w / 2)
            locker_pos_x = self.start_pos - locker_modifier
            # random assign position.
            locker.position = randint(0, 2)
            y_modifier = 0
            if locker.position == 0:
                y_modifier -= 30
            elif locker.position == 2:
                y_modifier += 30

            locker.rect = pygame.Rect(locker_pos_x, locker_pos_y + y_modifier, locker.l, locker.w)

            selector_pos_y = SCREEN_CENTER_Y - (locker.w * 1.5)
            selector_pos_x = self.start_pos - selector_modifier
            locker.selector.rect = pygame.Rect(selector_pos_x, selector_pos_y, locker.selector.l, locker.selector.w)

            self.lockers_list.append(locker)

            if i == 0:
                locker.is_selected = True

            locker_modifier += LOCKERS_LENGHT * 2
            selector_modifier += LOCKERS_LENGHT * 2


# locker entity.
class Locker:

    def __init__(self):
        self.l = LOCKERS_LENGHT
        self.w = LOCKERS_WIDTH
        # self.modifier = self.l * 1.5
        self.selector = Selector()
        self.is_selected = False
        self.rect = None
        self.position = None


# selector entity.
class Selector:

    def __init__(self):
        self.l = LOCKERS_LENGHT * 1.5
        self.w = LOCKERS_WIDTH * 3
        self.modifier = LOCKERS_LENGHT * 1.7
        self.rect = None


# full scene.
class TestScene(Game.Scene):

    def __init__(self):
        super().__init__()
        # font.
        self._font = Render.Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf")
        # grid.
        self._grid = Grid()

    def _load_resources(self):
        # grid Rect.
        self._grid.rect = pygame.Rect(self._grid.x, self._grid.y, self._grid.l, self._grid.w)
        self._grid.init_lockers(LOCKERS_NB)

    def update(self):
        # UP !
        if IO.Keyboard.is_down(K_UP):
            i = 0
            for l in self._grid.lockers_list:
                print(i)
                if l.is_selected:
                    if l.position > LOCKER_UP:
                        l.rect.y -= 30
                        l.position -= 1
                    l.is_selected = False

                    if i < len(self._grid.lockers_list) - 1:
                        self._grid.lockers_list[i+1].is_selected = True
                    else:
                        self._grid.lockers_list[0].is_selected = True
                    break
                i += 1
        # DOWN !
        elif IO.Keyboard.is_down(K_DOWN):
            i = 0
            for l in self._grid.lockers_list:
                print(i)
                if l.is_selected:
                    if l.position < LOCKER_DOWN:
                        l.rect.y += 30
                        l.position += 1
                    l.is_selected = False

                    if i < len(self._grid.lockers_list) - 1:
                        self._grid.lockers_list[i+1].is_selected = True
                    else:
                        self._grid.lockers_list[0].is_selected = True
                    break
                i += 1

    def draw(self):
        self._font.draw_text("test", (380, 20), (255, 0, 0))
        pygame.draw.rect(App.get_display(), (255, 0, 0), self._grid, 1)

        for x in self._grid.lockers_list:
            pygame.draw.rect(App.get_display(), (0, 255, 255), x.rect)
            if x.is_selected:
                pygame.draw.rect(App.get_display(), (0, 0, 255), x.selector.rect, 1)
