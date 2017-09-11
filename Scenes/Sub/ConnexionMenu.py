from PyGnin import *


COLOR_RED = (192, 57, 43)
COLOR_GREEN = (39, 174, 96)
COLOR_ORANGE = (211, 84, 0)
COLOR_PURPLE = (142, 68, 173)
COLOR_BLUE = (41, 128, 185)
COLOR_BLACK = (44, 62, 80)
COLOR_WHITE = (236, 240, 241)
COLOR_GREY = (127, 140, 141)


class ConnexionMenu(Game.SubScene):
    def __init__(self):
        super().__init__()
        self.nb_user_connected = 0
        self.createServerButton = None
        self.serverIpInput = None
        self.serverPortInput = None
        self.pseudoInput = None
        self.pseudoLabel = None
        self.connectClientButton = None
        self.usersListLabel = None
        self.usersLabels = []
        self._alert = None
        self._lunchGameButtonShowed = False

    def _initiate_data(self, **kargs):
        self.nb_user_connected = 0
        self.createServerButton = Gui.Button(label="Create server", pos=(10, 15), col=COLOR_RED)
        self.serverIpInput = Gui.InputBox(default="127.0.0.1", pos=(130, 10), background_col=COLOR_GREY)
        self.serverIpInput.text = "127.0.0.1"
        self.serverPortInput = Gui.SizeInput(default="1234", pos=(310, 10), size=(60, 30), background_col=COLOR_GREY)
        self.serverPortInput.text = "1234"
        self.pseudoInput = Gui.InputBox(
            default="Player",
            pos=(190, 40),
            label="Pseudo : ",
            label_side="left",
            background_col=COLOR_GREY
        )
        self.pseudoInput.text = "Player"
        self.pseudoLabel = Gui.Label(text="Pseudo : ", pos=(131, 46))
        self.connectClientButton = Gui.Button(label="Connect", pos=(380, 15), col=COLOR_RED)
        self.lunchGameButton = Gui.Button(label="Lunch party", pos=(500, 15), col=COLOR_ORANGE)
        self.usersListLabel = Gui.Label(text="Users list", pos=(10, 90))
        self.usersLabels = [
            Gui.Label(text="1 : ...", pos=(30, 120)),
            Gui.Label(text="2 : ...", pos=(30, 150)),
            Gui.Label(text="3 : ...", pos=(30, 180)),
            Gui.Label(text="4 : ...", pos=(30, 210))
        ]
        self._lunchGameButtonShowed = False

    def activate(self):
        App.show_cursor(True)
        self.nb_user_connected = 0
        self.createServerButton.add()
        self.connectClientButton.add()
        self.pseudoInput.add()
        self.serverIpInput.add()
        self.serverPortInput.add()

    def close(self):
        self.createServerButton.remove(False)
        self.connectClientButton.remove(False)
        self.pseudoInput.remove(False)
        self.pseudoLabel.remove(False)
        self.usersListLabel.remove(False)
        self.serverIpInput.remove(False)
        self.serverPortInput.remove(False)
        self.lunchGameButton.remove(False)
        for label in self.usersLabels:
            label.remove(False)

    def client_connected(self):
        self.connectClientButton.config(label="Disconnect", col=COLOR_GREEN)
        self.pseudoLabel.config(text="Pseudo : {0}".format(self.pseudoInput.text))
        self.pseudoInput.remove(False)
        self.pseudoLabel.add(fade=False)
        self.usersListLabel.add(fade=False)
        for label in self.usersLabels:
            label.add(fade=False)

    def toggle_server(self, is_open=True):
        if is_open:
            self.createServerButton.config(label="Close server", col=COLOR_GREEN)
        else:
            self.createServerButton.config(label="Create server", col=COLOR_RED)

    def client_closed(self):
        self.connectClientButton.config(label="Connect", col=COLOR_RED)
        self.usersListLabel.remove(False)
        self.pseudoInput.add(fade=False)
        self.pseudoLabel.remove(False)
        self.lunchGameButton.remove(False)
        for label in self.usersLabels:
            label.remove(False)

    def error_alert(self, title, desc):
        self._alert = Gui.Dialog(
            title=title,
            widget=Gui.Label(text=desc, col=COLOR_BLACK),
            pos=(50, 50)
        ).add()

    def set_users(self, nb=0, user1="...", user2="...", user3="...", user4="..."):
        self.usersListLabel.config(text="Users list : {0}/4".format(nb))
        self.usersLabels[0].config(text="1 : {0}".format(user1))
        self.usersLabels[1].config(text="2 : {0}".format(user2))
        self.usersLabels[2].config(text="3 : {0}".format(user3))
        self.usersLabels[3].config(text="4 : {0}".format(user4))

    def add_user_connected(self, place, pseudo):
        self.usersLabels[place].config(text="{0} : {1}".format(place + 1, pseudo))

    def set_nb_players(self, nb):
        self.usersListLabel.config(text="Users list : {0}/4".format(nb))
        if nb == 4 and not self._lunchGameButtonShowed:
            self.lunchGameButton.add()
            self._lunchGameButtonShowed = True
        elif nb < 4 and self._lunchGameButtonShowed:
            self._lunchGameButtonShowed = False
            self.lunchGameButton.remove()

    def draw(self):
        App.get_display().fill(COLOR_BLACK)
        Gui.update(App.get_time())
