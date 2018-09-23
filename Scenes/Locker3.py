from PyGnin import *
from random import randint
import pygame

LOCKERS_NB = 30
LOCKERS_LENGHT = 10
LOCKERS_WIDTH = 40

LOCKER_UP = 0
LOCKER_MID = 1
LOCKER_DOWN = 2

WAITING_STATE = 0
WINNING_STATE = 1
MAX_TIMER = 1000

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

        self.lockers_list = [Locker() for _ in range(LOCKERS_NB)]
        self.lockers_win = [randint(0, 2) for _ in range(LOCKERS_NB)]
        self.locker_win_nb = 0
        self.selected_locker = 0

    # init a list of lockers, depend of LOCKERS_NB.
    def init_lockers(self):
        locker_modifier = LOCKERS_LENGHT * 1.5
        selector_modifier = LOCKERS_LENGHT * 1.7
        App.show_cursor(True)

        for index in range(len(self.lockers_list)):
            locker = self.lockers_list[index]
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
            # winning pos footprint
            y_footprint = 0
            if self.lockers_win[index] == 0:
                y_footprint -= 30
            elif self.lockers_win[index] == 2:
                y_footprint += 30
            locker.footprint = pygame.Rect(locker_pos_x, locker_pos_y + y_footprint, locker.l, locker.w)

            selector_pos_y = SCREEN_CENTER_Y - (locker.w * 1.5)
            selector_pos_x = self.start_pos - selector_modifier
            locker.selector.rect = pygame.Rect(selector_pos_x, selector_pos_y, locker.selector.l, locker.selector.w)

            # set blocked type odd.
            # if index % 2:
            #     locker.blocked_type = True

            locker_modifier += LOCKERS_LENGHT * 2
            selector_modifier += LOCKERS_LENGHT * 2


# locker entity.
class Locker:

    def __init__(self):
        self.l = LOCKERS_LENGHT
        self.w = LOCKERS_WIDTH
        self.selector = Selector()
        self.win_position = False
        self.rect = None
        self.footprint = None
        self.discover = False
        self.position = None
        self.blocked_type = False


# selector entity.
class Selector:

    def __init__(self):
        self.l = LOCKERS_LENGHT * 1.5
        self.w = LOCKERS_WIDTH * 3
        self.rect = None


# full scene.
class Locker3(Game.Scene):

    def __init__(self):
        super().__init__()
        # font.
        self._font = Render.Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf")
        # grid.
        self._grid = Grid()
        self._state = WAITING_STATE
        self._elapsed_time = 0

    def _load_resources(self):
        self._grid.rect = pygame.Rect(self._grid.x, self._grid.y, self._grid.l, self._grid.w)
        self._grid.init_lockers()

    def update(self):
        if IO.Keyboard.is_down(K_ESCAPE):
            App.exit()

        if self._state == WAITING_STATE and MAX_TIMER > self._elapsed_time / 1000:
            self._elapsed_time += App.get_time()

            i = self._grid.selected_locker
            l = self._grid.lockers_list[i]
            # mirror.
            print(len(self._grid.lockers_list) - i)
            mirror = self._grid.lockers_list[len(self._grid.lockers_list) - 1 - i]

            if self._grid.locker_win_nb == LOCKERS_NB:
                self._state = WINNING_STATE

            # if l.win_position:
            #     if i < len(self._grid.lockers_list) - 1:
            #         self._grid.selected_locker += 1
            #     else:
            #         self._grid.selected_locker = 0
            #     return

            # UP !
            if IO.Keyboard.is_down(K_UP):
                # locker.
                if l.position > LOCKER_UP:
                    l.rect.y -= 30
                    l.position -= 1
                elif l.blocked_type:
                    return
                else:
                    l.rect.y += 60
                    l.position = LOCKER_DOWN

                # mirror locker.
                if mirror.position > LOCKER_UP:
                    mirror.rect.y -= 30
                    mirror.position -= 1
                elif mirror.blocked_type:
                    return
                else:
                    mirror.rect.y += 60
                    mirror.position = LOCKER_DOWN

                if i < len(self._grid.lockers_list) - 1:
                    self._grid.selected_locker += 1
                else:
                    self._grid.selected_locker = 0

                if l.position == self._grid.lockers_win[i]:
                    l.win_position = True
                    l.discover = True
                    self._grid.locker_win_nb += 1
                else:
                    if l.win_position:
                        l.win_position = False
                        self._grid.locker_win_nb -= 1

            # DOWN !
            elif IO.Keyboard.is_down(K_DOWN):
                # locker.
                if l.position < LOCKER_DOWN:
                    l.rect.y += 30
                    l.position += 1
                elif l.blocked_type:
                    return
                else:
                    l.rect.y -=60
                    l.position = LOCKER_UP

                # mirror locker.
                if mirror.position < LOCKER_DOWN:
                    mirror.rect.y += 30
                    mirror.position += 1
                elif mirror.blocked_type:
                    return
                else:
                    mirror.rect.y -=60
                    mirror.position = LOCKER_UP

                if i < len(self._grid.lockers_list) - 1:
                    self._grid.selected_locker += 1
                else:
                    self._grid.selected_locker = 0

                if l.position == self._grid.lockers_win[i]:
                    l.win_position = True
                    l.discover = True
                    self._grid.locker_win_nb += 1
                else:
                    if l.win_position:
                        l.win_position = False
                        self._grid.locker_win_nb -= 1

    def draw(self):
        self._font.draw_text("%.2f" % (MAX_TIMER - (self._elapsed_time / 1000)), (10, 10), (255, 0, 0))

        if self._state == WAITING_STATE and MAX_TIMER >= self._elapsed_time / 1000:
            self._font.draw_text("jean boloss", (330, 20), (255, 0, 0))
            pygame.draw.rect(App.get_display(), (255, 0, 0), self._grid, 1)

            for index in range(len(self._grid.lockers_list)):
                locker = self._grid.lockers_list[index]
                if locker.discover:
                    pygame.draw.rect(App.get_display(), (91, 91, 91), locker.footprint)
                pygame.draw.rect(App.get_display(), (0, 255, 0) if locker.win_position else (0, 255, 255), locker.rect)

                if index == self._grid.selected_locker:
                    pygame.draw.rect(App.get_display(), (0, 0, 255), locker.selector.rect, 1)
        elif self._state == WINNING_STATE:
            self._font.draw_text("GG PD", (330, 20), (255, 0, 0))
            pygame.draw.rect(App.get_display(), (255, 0, 0), self._grid, 1)
        else:
            self._font.draw_text("PAS GG PD", (330, 20), (255, 0, 0))
            pygame.draw.rect(App.get_display(), (255, 0, 0), self._grid, 1)
