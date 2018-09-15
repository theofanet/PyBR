from PyGnin import *
import pygame

MLTP = 3
DIFFICULTY = 4

LOCKER_LENGHT = 10
LOCKER_WIDTH = 40

class TestScene(Game.Scene):

    def __init__(self):
        super().__init__()

        # screen size.
        self._screenW = 600
        self._screenL = 800

        # font.
        self._font = Render.Font("assets/Permanent_Marker/PermanentMarker-Regular.ttf")

        # nb lockers for a grid.
        self._nbLockers = DIFFICULTY * MLTP
        self._lockersList = list()

        # set grid size.
        self._gridLenght = self._nbLockers * LOCKER_LENGHT * 2
        self._gridWidth = LOCKER_WIDTH * 2

        # set grid position.
        self._xcenter = self._screenL / 2
        self._ycenter = self._screenW / 2
        self._gridY = self._ycenter - (self._gridWidth / 2)
        self._gridX = self._xcenter - (self._gridLenght / 2)

        # set selector size.
        self._selectLenght = LOCKER_LENGHT * 1.5
        self._selectWidth = LOCKER_WIDTH * 3

    def _load_resources(self):
        self._grid = pygame.Rect(self._gridX, self._gridY, self._gridLenght, self._gridWidth)
        self._selector = pygame.Rect((self._xcenter + (self._gridLenght / 2) - (LOCKER_LENGHT * 1.7)), self._ycenter - (self._selectWidth / 2), self._selectLenght, self._selectWidth)

    def update(self):
        # TODO: refact tout ce bordel avec la merde du dessus.
        start = self._xcenter + (self._gridLenght / 2)
        selectModifier = LOCKER_LENGHT * 1.7
        lockerModifier = LOCKER_LENGHT * 1.5
        ly = self._ycenter - (LOCKER_WIDTH / 2)

        # TODO: switch selected locker state and move selector next.
        if IO.Keyboard.is_down(K_LEFT):
            if self._selector.x < (start - selectModifier) - (selectModifier * self._nbLockers):
                self._selector.x = start - selectModifier
            else:
                self._selector.x -= LOCKER_LENGHT * 2
        elif IO.Keyboard.is_down(K_RIGHT):
            if self._selector.x < start - selectModifier:
                self._selector.x += LOCKER_LENGHT * 2

        # lockers positions.
        # TODO: update lockers up and down. [is_selected]
        # TODO: switch les rec dans le load ou init.
        self._lockersList = list() # reset.
        for i in range(self._nbLockers):
            lx = (self._xcenter + (self._gridLenght / 2) - lockerModifier)
            locker = pygame.Rect(lx, ly, LOCKER_LENGHT, LOCKER_WIDTH)
            self._lockersList.append(locker)
            lockerModifier += LOCKER_LENGHT * 2

    def draw(self):
        self._font.draw_text("test", (380, 20), (255, 0, 0))
        pygame.draw.rect(App.get_display(), (255, 0, 0), self._grid, 1)
        pygame.draw.rect(App.get_display(), (0, 0, 255), self._selector, 1)

        for x in self._lockersList:
            pygame.draw.rect(App.get_display(), (0, 255, 255), x)
