from PyGnin import *
import pygame
import random
import math


# TODO: Rock est en effet un sprite. Cependant le fichier et donc la class devrait
# TODO : se trouver dans le dossier (module) Sprites, comme Player ;)
# TODO: Rock est bien un sprite. Cependant il doit reprenster, comme son nom l'indique, une rock, pas toute les rock
# TODO : C'est ta class generate qui doit generer les differentes instances de Rock et
# TODO : retourner un tableaux de ceux-ci a la map pour qu'elle les dessines
class Rock(Game.Sprite):

    def __init__(self, nb_items, min_range_between=300, x=(0, 3200), y=(0, 3200)):
        super().__init__()

        self.debug_rocks_shapes = False  # toggle K_r
        self.debug_rocks_values = False  # pas de toggle
        self._rock_tileset = Render.TileSet("assets/rocks_rotated.png", (256, 256))
        self._rock_tileset.set_scale(0.4)
        self._tile_range = (0, 7)
        self._min_range_between_rocks = min_range_between
        self._max_nb_rocks = nb_items
        self._x_rect_size = x
        self._y_rect_size = y
        self._rocks = [{"tile": [0, 0], "pos": [0, 0]} for x in range(self._max_nb_rocks)]

    @staticmethod
    def calc_dist(p1, p2):

        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    def generate(self):

        used_pos = []
        for rock in self._rocks:

            keep_going = True

            tile_x = random.randint(self._tile_range[0], self._tile_range[1])
            tile_y = random.randint(self._tile_range[0], self._tile_range[1])

            while keep_going:

                # NEW ALGO
                current_pos = list()

                if not current_pos:
                    current_pos = (random.randint(self._x_rect_size[0], self._x_rect_size[1]),
                                   random.randint(self._y_rect_size[0], self._y_rect_size[1]))

                    # LOG ##############################
                    if self.debug_rocks_values:
                        print("current" + repr(current_pos))
                    # ##################################

                    if used_pos:

                        for pos in used_pos:
                            dist = int(self.calc_dist(current_pos, pos))

                            # LOG ###########################################################################
                            if self.debug_rocks_values:
                                print("current:" + repr(current_pos) + " used:" + repr(pos) + " dist:" + repr(int(dist)))
                            # ###############################################################################

                            # if dist not in range(self._range_between_rocks[0], self._range_between_rocks[1]):
                            if dist < self._min_range_between_rocks:
                                # LOG #########################################################
                                if self.debug_rocks_values:
                                    print("bad_range = " + repr(dist)
                                          + " !(" + repr(self._min_range_between_rocks)
                                          + " <> " + repr(self._min_range_between_rocks) + ")")
                                # #############################################################
                                current_pos = list()
                                break

                # NEXT
                if current_pos:
                    used_pos.append(current_pos)

                    # LOG #########
                    if self.debug_rocks_values:
                        print("LIST POINTS ====> " + repr(used_pos))
                        print("LIST LEN    ====> " + repr(len(used_pos)))
                    # #############

                    keep_going = False

            rock["tile"][0] = tile_x
            rock["tile"][1] = tile_y
            rock["pos"][0] = current_pos[0]
            rock["pos"][1] = current_pos[1]

        # LOG ############
        if self.debug_rocks_values:
            print(self._rocks)
        # ################

    def draw(self, surface, camera=None):

        if IO.Keyboard.is_down(K_r):
            self.debug_rocks_shapes = not self.debug_rocks_shapes

        tile_w, tile_h = self._rock_tileset.get_tile_size()

        for rock in self._rocks:

            tile_x = rock["tile"][0]
            tile_y = rock["tile"][1]
            pos_x = rock["pos"][0]
            pos_y = rock["pos"][1]

            if camera:
                pos_x -= camera.get_position()[0]
                pos_y -= camera.get_position()[1]

            pos_x -= tile_w / 2
            pos_y -= tile_h / 2

            # DEBUG ##############
            if self.debug_rocks_shapes:
                a = (pos_x, pos_y)
                c = (pos_x + tile_w, pos_y + tile_h)
                pygame.draw.circle(surface, (255, 0, 0),
                                   (int((a[0] + c[0]) / 2), int((a[1] + c[1]) / 2)),
                                   self._range_between_rocks[0], 2) # TODO : Bug car self ne contient pas de _range_between_rocks
            # ####################

            self._rock_tileset.draw_tile(tile_x, tile_y, pos_x, pos_y, screen=surface)
            pygame.draw.rect(surface, (0, 0, 0), (pos_x, pos_y, tile_w, tile_h), 2)
