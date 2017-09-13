from PyGnin import *


# class Rock(Game.Sprite):
#
#     def __init__(self):
#         super().__init__()
#         self.load_image('assets/rock_test.jpg')
#         self.set_scale(0.2)


class Guiboude(Game.Scene):

    def __init__(self):
        super().__init__()

        # simple rock !!!!
        # self.rock = Rock()
        # self.add_sprites(self.rock)
        # self.rock_image = Render.Image('assets/rock_test.jpg')
        # self._direction = None

        #tilset rock !!!!
        self._rock_tileset = Render.TileSet('assets/rocks_rotated.png', (256, 256))
        self._rock_tileset.set_scale(0.2)
        # self._time = 0
        # self._tilePos = [4, 2]

        # rocks = [{"tile": [0, 0], "pos": [0, 0]} for x in range(200)]
        # for rock in rocks:
        #     rock["tile"][0] = 4
        #     rock["tile"][1] = 2
        #     rock["pos"][0] = 50
        #     rock["pos"][1] = 50

        # menu
        self._nameInput = Gui.InputBox(label="Name : ", pos=(200, 400), label_side="left")
        self._button = Gui.Button(label="pick me", pos=(450, 400), col=(100, 0, 0))
        self._button.on_click = self.button_clicked

        #camera
        self._camera = Render.Camera((200, 200), 5)

    def _load_resources(self):
        # self.rock.set_position(50, 50)

        App.show_cursor(True)
        self._nameInput.add()
        self._button.add()

    def close_scene(self):
        self._nameInput.remove()
        self._button.remove()

    def update(self): pass

        # tileset rock !!!!
        # self._time += App.get_time()
        #
        # if self._time > 2000:
        #     self._tilePos[0] += 1
        #     self._tilePos[1] += 1
        #     self._time = 0
        #
        # if self._tilePos[0] > 7:
        #     self._tilePos[0] = 0
        #     self._tilePos[1] = 0
            ####

        #test camera
        # x, y = self.rock.get_position()
        #
        # if IO.Keyboard.is_held(K_s):
        #     y += 5
        #     self._direction = DIR_DOWN
        # elif IO.Keyboard.is_held(K_w):
        #     y -= 5
        #     self._direction = DIR_UP
        # elif IO.Keyboard.is_held(K_a):
        #     x -= 5
        #     self._direction = DIR_LEFT
        # elif IO.Keyboard.is_held(K_d):
        #     x += 5
        #     self._direction = DIR_RIGHT
        #
        # if IO.Keyboard.is_up(K_a) \
        #         or IO.Keyboard.is_up(K_d) \
        #         or IO.Keyboard.is_up(K_w) \
        #         or IO.Keyboard.is_up(K_s):
        #     self._direction = None
        #
        # self.rock.set_position(x, y)
        # self._camera.update(self.rock.get_position(), self._direction)

    def draw(self):
        App.get_display().fill((0, 0, 0))
        # super().draw()

        super().draw_sprites(self._camera)

        # self.rock_image.draw(50, 50)

        # self._rock_tileset.draw_tiled(self._tilePos[0], self._tilePos[1], self._position[0], self._position[1])

        #tiles with camera
        x, y = (50, 50)
        x -= self._camera.get_position()[0]
        y -= self._camera.get_position()[1]
        self._rock_tileset.draw_tile(4, 2, x, y)

        # button
        Gui.update(App.get_time())

    def button_clicked(self):
        print(self._nameInput.text)