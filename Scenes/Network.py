from PyGnin import *
import Scenes.Sub


class NetPkgHandler(Network.PkgHandler):
    def __init__(self, master=None, scene=None):
        super().__init__(master)
        self._scene = scene

    def receive(self, pkg):
        if "type" in pkg:
            if self._scene.active_subScene == self._scene.game_subScene:
                if pkg["type"] == "players_update" and "data" in pkg:
                    self._scene.game_subScene.update_players(pkg["data"])
                    self._scene.waitingPlayersData = False
                elif pkg["type"] == "player_update" and "token" in pkg and "data" in pkg:
                    self._scene.game_subScene.update_player(pkg["token"], pkg["data"])
                    self._scene.waitingPlayersData = False
            else:
                if pkg["type"] == "users_list" and "list" in pkg:
                    i = nb = 0
                    self._scene.connexion_menu.set_users()
                    for pseudo in pkg["list"]:
                        if pseudo !=  "...":
                            self._scene.connexion_menu.add_user_connected(i, pseudo)
                            nb += 1
                        i += 1
                    self._scene.connexion_menu.set_nb_players(nb)
                elif pkg["type"] == "game_start":
                    self._scene.game_subScene.set_players(pkg["data"], self._master.get_token())
                    self._scene.lunch_game()
                
                
class ServerPlayer(object):
    def __init__(self, token):
        super().__init__()
        self._position = (0, 0)
        self._direction = None
        self._token = token
    
    def set_position(self, pos):
        self._position = pos
    
    def get_position(self):
        return self._position

    def get_token(self):
        return self._token

    def serialize(self):
        return {
            "position": self._position,
            "token": self._token
        }


class NetServerHandler(Network.ServerHandler):
    def __init__(self, server=None):
        super().__init__(server)
        self._players = {}
        self._nbPlayer = 0
        self._time = 0
        self._players_ready = 0
        self._gameStarted = False
        
    def player_connected(self, client):
        self._players[client.get_socket()] = ServerPlayer(token=client.get_token())
        self._nbPlayer += 1
        
    def player_disconnected(self, client):
        if client.get_socket() in self._players.keys():
            del self._players[client.get_socket()]
            self._nbPlayer -= 1
            
    def handle_package(self, client, pkg):
        if client.get_socket() in self._players.keys():
            player = self._players[client.get_socket()]
            if "action" in pkg:
                if pkg["action"] == "set_position" and "position" in pkg:
                    player.set_position(pkg["position"])
                if pkg["action"] == "get_players_data":
                    players_data = []
                    for sock, p in self._players.items():
                        players_data.append(p.serialize())
                    client.send_pkg({
                        "type": "players_update",
                        "data": players_data
                    })
                if pkg["action"] == "set_ready":
                    self._players_ready += 1
                    if self._players_ready == 4:
                        self._gameStarted = True
                        players_data = []
                        for sock, p in self._players.items():
                            players_data.append(p.serialize())
                        self._server.send_to_all({
                            "type": "game_start",
                            "data": players_data
                        })
            self._players[client.get_socket()] = player
        

class NetworkScene(Game.Scene):
    def __init__(self):
        super().__init__()
        self._time = 0

        self._server = Network.Server(max_listen=4, handler=NetServerHandler())
        self._client = Network.Client(pkg_handler=NetPkgHandler(scene=self))
        self._client.after_close = self.on_client_close

        self.is_server = False
        self.connexion_menu = Scenes.Sub.ConnexionMenu()
        self.game_subScene = Scenes.Sub.GameSubScene()

        self.waitingPlayersData = False

    def _load_resources(self):
        App.show_cursor(True)
        self.active_subScene = self.connexion_menu
        self.connexion_menu.initiate(self)
        self.connexion_menu.activate()
        self.connexion_menu.createServerButton.on_click = self.create_server
        self.connexion_menu.connectClientButton.on_click = self.connect_client
        self.connexion_menu.lunchGameButton.on_click = self.set_ready

    def get_camera(self):
        if self.active_subScene == self.game_subScene:
            return self.game_subScene.get_camera()

    def close_scene(self):
        if self.active_subScene:
            self.active_subScene.close()
        self._client.close()
        self._server.close()

    def draw(self):
        if self.active_subScene:
            self.active_subScene.draw()

    def update(self):
        if not self.active_subScene or self.active_subScene.update():
            super().update()

        if self.active_subScene == self.game_subScene:
            self._time += App.get_time()

            if not self.waitingPlayersData or self._time > 250:
                self._client.send_pkg({"action": "get_players_data"})
                self.waitingPlayersData = True
                self._time = 0

            self._client.send_pkg({
                "action": "set_position",
                "position": self.game_subScene.player.get_position()
            })

    def create_server(self):
        if self._server.is_closed():
            self._server.start(self.connexion_menu.serverIpInput.text, int(self.connexion_menu.serverPortInput.text))
            self._server.run()
            self.connexion_menu.toggle_server(True)
            self.is_server = True
        else:
            self._server.close()
            self.connexion_menu.toggle_server(False)

    def on_client_close(self):
        self._client = Network.Client(pkg_handler=NetPkgHandler(scene=self))
        self.connexion_menu.client_closed()

    def connect_client(self):
        if not self._client.is_connected():
            if self._client.connect(
                    self.connexion_menu.pseudoInput.text,
                    self.connexion_menu.serverIpInput.text,
                    int(self.connexion_menu.serverPortInput.text)
            ):
                self._client.run()
                self._client.send_pkg({"action": "get_users_list"})
                self.connexion_menu.client_connected()
            else:
                self.connexion_menu.error_alert("error", self._client.get_last_error())
        else:
            self._client.close()

    def set_ready(self):
        self._client.send_pkg({"action": "set_ready"})

    def lunch_game(self):
        if not self.is_server:
            self.connexion_menu.close()
            self.game_subScene.initiate(self)
            self.game_subScene.activate()
            self.active_subScene = self.game_subScene
