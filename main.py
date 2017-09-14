from PyGnin import *
import Scenes
from configparser import ConfigParser


config = ConfigParser()
config.read("./config.ini")
Registry.register("config", config)


if __name__ == '__main__':
    App.init(
        size=list(map(int, config.get("window", "size").split(","))),
        background=list(map(int, config.get("window", "background").split(","))),
        mouse_visible=config.getboolean("window", "mouse_visible"),
        show_fps=config.getboolean("window", "show_fps"),
        fps=config.getint("window", "fps"),
        fullscreen=config.getboolean("window", "fullscreen"),
        title=config.get("window", "title")
    )

    # Loading scenes
    # App.load_scene("net", Scenes.NetworkScene())
    App.load_scene("first", Scenes.FirstScene())
    App.set_active_scene("first")

    App.run()
