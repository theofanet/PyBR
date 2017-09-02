from PyGnin import *

import Scenes


if __name__ == '__main__':
    App.init(
        size=(840, 480),
        background=(255, 255, 255),
        mouse_visible=True,
        show_fps=True,
        fps=60
    )

    # Loading scenes
    App.load_scene("main", Scenes.FirstScene())
    App.set_active_scene("main")

    App.run()
