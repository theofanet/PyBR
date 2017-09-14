from PyGnin import *
import pygame


class SoloSettings(Game.SubScene):
    def __init__(self):
        super().__init__()
        self.returnButton = Gui.Button(label="Return", pos=(10, App.get_screen_size()[1] - 60))

        self._restartLabel = Gui.Label(
            text="Settings with * need the application to be restarted",
            pos=(App.get_screen_size()[0] - 320, App.get_screen_size()[1] - 90)
        )

        self._saveButton = Gui.Button(label="Save", pos=(App.get_screen_size()[0] - 120, App.get_screen_size()[1] - 60))
        self._saveButton.on_click = self.save_settings

        # AIMS IMG AND BUTTONS
        self._aimLabel = Gui.Label(text="Aim type", pos=(10, 5))
        self._aimsTileSet = Render.TileSet("assets/aims.png", (188, 200))
        self._aimsTileSet.set_scale(0.2)
        self._selected_aim = list(Registry.registered("config").get("aim", "type").split(","))
        self._aimsButton = [
            Gui.SizeButton(label=" ", pos=(30, 29), size=(40, 40)),
            Gui.SizeButton(label=" ", pos=(80, 29), size=(40, 40)),
            Gui.SizeButton(label=" ", pos=(131, 30), size=(40, 40)),
            Gui.SizeButton(label=" ", pos=(31, 79), size=(40, 40)),
            Gui.SizeButton(label=" ", pos=(81, 80), size=(40, 40)),
            Gui.SizeButton(label=" ", pos=(131, 80), size=(40, 40)),
            Gui.SizeButton(label=" ", pos=(31, 130), size=(40, 40)),
            Gui.SizeButton(label=" ", pos=(81, 130), size=(40, 40)),
            Gui.SizeButton(label=" ", pos=(131, 130), size=(40, 40))
        ]
        self._aimsButton[0].on_click = self.select_aim_00
        self._aimsButton[1].on_click = self.select_aim_10
        self._aimsButton[2].on_click = self.select_aim_20
        self._aimsButton[3].on_click = self.select_aim_01
        self._aimsButton[4].on_click = self.select_aim_11
        self._aimsButton[5].on_click = self.select_aim_21
        self._aimsButton[6].on_click = self.select_aim_02
        self._aimsButton[7].on_click = self.select_aim_12
        self._aimsButton[8].on_click = self.select_aim_22

        # COLORS SCALES AND LABELS
        r, g, b = list(map(int, Registry.registered("config").get("aim", "color").split(",")))
        self._aimColorLabel = Gui.Label(text="Aim color", pos=(10, 185))
        self._aimColorLabelRed = Gui.Label(text="Red", pos=(20, 220))
        self._aimsColorR = Gui.Scale(min=0, max=255, min_step=1, show_value=True, pos=(100, 200), col=(100, 0, 0))
        self._aimsColorR.value = r
        self._aimColorLabelGreen = Gui.Label(text="Green", pos=(20, 270))
        self._aimsColorG = Gui.Scale(min=0, max=255, min_step=1, show_value=True, pos=(100, 250), col=(0, 100, 0))
        self._aimsColorG.value = g
        self._aimColorLabelBlue = Gui.Label(text="Blue", pos=(20, 320))
        self._aimsColorB = Gui.Scale(min=0, max=255, min_step=1, show_value=True, pos=(100, 300), col=(0, 0, 100))
        self._aimsColorB.value = b

        # SHOW FPS SWITCH
        self._showFpsLabel = Gui.Label(text="Show FPS", pos=(350, 15))
        self._showFpsSwitch = Gui.Switch(
            state=Registry.registered("config").getboolean("window", "show_fps"),
            pos=(450, 10)
        )

        # FULL SCREEN SWITCH
        self._fullScreenLabel = Gui.Label(text="* Full screen", pos=(350, 45))
        self._fullScreenSwitch = Gui.Switch(
            state=Registry.registered("config").getboolean("window", "fullscreen"),
            pos=(450, 40)
        )

        # MAP SETTINGS
        self._mapLabel = Gui.Label(text="Map", pos=(350, 100))
        self._mapFrequencyLabel = Gui.Label(text="Frequency", pos=(350, 150))
        self._mapFrequencyScale = Gui.Scale(min=0, max=300, min_step=0.1, show_value=True, pos=(450, 132))
        self._mapFrequencyScale.value = Registry.registered("config").getfloat("map", "frequency")

        self._mapWaterLvlLabel = Gui.Label(text="Water lvl", pos=(350, 200))
        self._mapWaterLvlScale = Gui.Scale(min=-1.0, max=1.0, min_step=0.1, show_value=True, pos=(450, 182))
        self._mapWaterLvlScale.value = Registry.registered("config").getfloat("map", "water_level")

        self._reloadMapLabel = Gui.Label(text="Reload map", pos=(470, 100))
        self.reloadMapSwitch = Gui.Switch(state=False, pos=(550, 96))

    def activate(self):
        App.show_cursor(True)
        self._selected_aim = list(Registry.registered("config").get("aim", "type").split(","))
        r, g, b = list(map(int, Registry.registered("config").get("aim", "color").split(",")))
        self._aimsColorR.value = r
        self._aimsColorG.value = g
        self._aimsColorB.value = b
        self._showFpsSwitch.config(state=Registry.registered("config").getboolean("window", "show_fps"))
        self._fullScreenSwitch.config(state=Registry.registered("config").getboolean("window", "fullscreen"))
        self._mapFrequencyScale.value = Registry.registered("config").getfloat("map", "frequency")
        self._mapWaterLvlScale.value = Registry.registered("config").getfloat("map", "water_level")
        self.add_gui()

    def add_gui(self):
        self.returnButton.add()
        self._saveButton.add()
        self._aimLabel.add()
        for button in self._aimsButton:
            button.add()
        self._aimColorLabel.add()
        self._aimColorLabelRed.add()
        self._aimsColorR.add()
        self._aimColorLabelGreen.add()
        self._aimsColorG.add()
        self._aimColorLabelBlue.add()
        self._aimsColorB.add()
        self._showFpsLabel.add()
        self._showFpsSwitch.add()
        self._fullScreenLabel.add()
        self._fullScreenSwitch.add()
        self._restartLabel.add()
        self._mapLabel.add()
        self._mapFrequencyLabel.add()
        self._mapFrequencyScale.add()
        self._mapWaterLvlLabel.add()
        self._mapWaterLvlScale.add()
        self.reloadMapSwitch.add()
        self._reloadMapLabel.add()

    def remove_gui(self):
        self.returnButton.remove(False)
        self._saveButton.remove(False)
        self._aimLabel.remove(False)
        for button in self._aimsButton:
            button.remove(False)
        self._aimColorLabel.remove(False)
        self._aimColorLabelRed.remove(False)
        self._aimsColorR.remove(False)
        self._aimColorLabelGreen.remove(False)
        self._aimsColorG.remove(False)
        self._aimColorLabelBlue.remove(False)
        self._aimsColorB.remove(False)
        self._showFpsSwitch.remove(False)
        self._showFpsLabel.remove(False)
        self._fullScreenLabel.remove(False)
        self._fullScreenSwitch.remove(False)
        self._restartLabel.remove(False)
        self._mapLabel.remove(False)
        self._mapFrequencyLabel.remove(False)
        self._mapFrequencyScale.remove(False)
        self._mapWaterLvlLabel.remove(False)
        self._mapWaterLvlScale.remove(False)
        self.reloadMapSwitch.remove(False)
        self._reloadMapLabel.remove(False)

    def close(self):
        self.remove_gui()

    def draw(self, camera=None, screen=None):
        if not screen:
            screen = App.get_display()

        screen.fill((0, 0, 0))
        Gui.update(App.get_time())

        ssr, ssc = self._selected_aim
        sx, sy = [int(ssr)*50 + 36, int(ssc)*50 + 34]
        pygame.draw.rect(screen, (10, 200, 20), pygame.Rect(sx, sy, 29, 30))

        self._aimsTileSet.draw_tile(0, 0, 50, 50, True, screen=screen)
        self._aimsTileSet.draw_tile(1, 0, 100, 50, True, screen=screen)
        self._aimsTileSet.draw_tile(2, 0, 150, 50, True, screen=screen)
        self._aimsTileSet.draw_tile(0, 1, 50, 100, True, screen=screen)
        self._aimsTileSet.draw_tile(1, 1, 100, 100, True, screen=screen)
        self._aimsTileSet.draw_tile(2, 1, 150, 100, True, screen=screen)
        self._aimsTileSet.draw_tile(0, 2, 50, 150, True, screen=screen)
        self._aimsTileSet.draw_tile(1, 2, 100, 150, True, screen=screen)
        self._aimsTileSet.draw_tile(2, 2, 150, 150, True, screen=screen)

        pygame.draw.rect(
            screen,
            (self._aimsColorR.value, self._aimsColorG.value, self._aimsColorB.value),
            pygame.Rect(75, 184, 25, 25)
        )

        super().draw(camera, screen)

    def select_aim_00(self):
        self._selected_aim = ["0", "0"]

    def select_aim_10(self):
        self._selected_aim = ["1", "0"]

    def select_aim_20(self):
        self._selected_aim = ["2", "0"]

    def select_aim_01(self):
        self._selected_aim = ["0", "1"]

    def select_aim_11(self):
        self._selected_aim = ["1", "1"]

    def select_aim_21(self):
        self._selected_aim = ["2", "1"]

    def select_aim_02(self):
        self._selected_aim = ["0", "2"]

    def select_aim_12(self):
        self._selected_aim = ["1", "2"]

    def select_aim_22(self):
        self._selected_aim = ["2", "2"]

    def save_settings(self):
        Registry.registered("config").set("aim", "type", ",".join(self._selected_aim))
        Registry.registered("config").set("aim", "color", ",".join([
            str(self._aimsColorR.value),
            str(self._aimsColorG.value),
            str(self._aimsColorB.value)
        ]))
        Registry.registered("config").set("window", "show_fps", str(self._showFpsSwitch.state))
        Registry.registered("config").set("window", "fullscreen", str(self._fullScreenSwitch.state))
        Registry.registered("config").set("map", "frequency", str(self._mapFrequencyScale.value))
        Registry.registered("config").set("map", "water_level", str(self._mapWaterLvlScale.value))
        App.show_fps(self._showFpsSwitch.state)
        with open('config.ini', 'w') as configfile:
            Registry.registered("config").write(configfile)

