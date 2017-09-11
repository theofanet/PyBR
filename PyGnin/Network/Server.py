import socket
import select
import json
from threading import Thread, RLock
import base64
import uuid


class ServerHandler(object):
    def __init__(self, server=None):
        self._server = server

    def set_server(self, server):
        self._server = server

    def handle_package(self, client, pkg): pass

    def player_connected(self, client): pass

    def player_disconnected(self, client): pass

    def update(self): pass


class SClient(object):
    def __init__(self, connexion, sock):
        self._connexion = connexion
        self._socket = sock
        self._pseudo = ""
        self._token = ""

    def set_token(self, token):
        self._token = token

    def get_token(self):
        return self._token

    def set_pseudo(self, pseudo):
        self._pseudo = pseudo

    def get_pseudo(self):
        return self._pseudo

    def get_socket(self):
        return self._socket

    def send_pkg(self, data):
        encoded_data = base64.b64encode(bytes(json.dumps(data) + "[END_BLOCK]", 'utf8'))
        self._socket.send(encoded_data)

    def close(self):
        self._socket.close()

    def receive_package(self):
        encoded_data = []
        decoded_data = []
        data = "DATABLOCK"
        #while len(data):
        try:
            data = self._socket.recv(1024)
            if data:
                encoded_data.append(data.decode("utf8"))
        except socket.error:
            data = ""
            #continue
        if len(encoded_data):
            try:
                encoded_data = base64.b64decode(bytes("".join(encoded_data), 'utf8'))
                for json_data in encoded_data.decode("utf8").split("[END_BLOCK]"):
                    if json_data != '':
                        decoded_data.append(json.loads(str(json_data)))
            except ValueError or TypeError as e:
                print("Unable to decode server message")
                print(e)
        return decoded_data


class ServerRunThread(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self._server = server

    def run(self):
        while not self._server.need_exit():
            with RLock():
                self._server.run_loop()
        self._server.final_close()


class Server(object):
    def __init__(self, hostname="localhost", port=1234, max_listen=5, handler=None):
        self._hostname = hostname
        self._port = port
        self._maxListen = max_listen
        self._connexion = None
        self._closed = True
        self._exit = False
        self._newClients = []
        self._connectedClients = []
        self._socketLinks = {}
        self._clientByPseudo = {}
        self._thread = ServerRunThread(self)
        self._users_list = ["..." for x in range(max_listen)]
        if not handler:
            handler = ServerHandler(self)
        handler.set_server(self)
        self._handler = handler

    def start(self, hostname=None, port=None):
        if hostname:
            self._hostname = hostname
        if port:
            self._port = port
        self._connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connexion.bind((self._hostname, self._port))
        self._connexion.listen(self._maxListen)
        self._closed = False

        print("###########################################")
        print("# Server listening")
        print("# Host : {0}".format(self._hostname))
        print("# Port : {0}".format(self._port))
        print("###########################################")

    def close(self):
        if not self._closed:
            print("Closing server")
            self.send_to_all({"type": "server_closing"})
            self._exit = True
            if self._thread.isAlive():
                self._thread.join()
                self._thread = ServerRunThread(self)

    def final_close(self):
        for sock in self._connectedClients:
            if sock in self._socketLinks:
                self.close_client(self._socketLinks[sock])
        self._connexion.close()
        self._closed = True

    def is_closed(self):
        return self._closed

    def need_exit(self):
        return self._exit

    def run(self):
        if not self._closed:
            self._thread.start()

    def send_to_all(self, pkg, except_client=False):
        for sock in self._connectedClients:
            if sock in self._socketLinks.keys():
                client = self._socketLinks[sock]
                if not except_client or client is not except_client:
                    client.send_pkg(pkg)

    def run_loop(self):
        waiting_connexions, w_list, x_list = select.select([self._connexion], [], [], 0.05)
        for co in waiting_connexions:
            client_socket, connexion_info = co.accept()
            client_socket.setblocking(False)
            self._newClients.append(client_socket)
            self._socketLinks[client_socket] = SClient(self._connexion, client_socket)

        try:
            client_to_connect, w_list, x_list = select.select(self._newClients, [], [], 0.05)
        except select.error:
            pass
        else:
            for c in client_to_connect:
                if c in self._socketLinks.keys():
                    client = self._socketLinks[c]
                    for pkg in client.receive_package():
                        self.handle_connexion(client, pkg)

        try:
            clients_to_read, w_list, x_list = select.select(self._connectedClients, [], [], 0.05)
        except select.error:
            pass
        else:
            for c in clients_to_read:
                if c in self._socketLinks.keys():
                    client = self._socketLinks[c]
                    for pkg in client.receive_package():
                        self.handle_package(client, pkg)

        if self._handler:
            self._handler.update()

    def close_client(self, client):
        if self._handler:
            self._handler.player_disconnected(client)
        client.close()
        if client.get_socket() in self._newClients:
            self._newClients.remove(client.get_socket())
        if client.get_socket() in self._connectedClients:
            i = self._connectedClients.index(client.get_socket())
            if 0 <= i < 4:
                self._users_list[i] = "..."
            self._connectedClients.remove(client.get_socket())
        if client.get_socket() in self._socketLinks.keys():
            del self._socketLinks[client.get_socket()]
        if client.get_pseudo() in self._clientByPseudo.keys():
            del self._clientByPseudo[client.get_pseudo()]

    def handle_package(self, client, pkg):
        if self._handler:
            self._handler.handle_package(client, pkg)
        if "action" in pkg:
            if pkg["action"] == "disconnect":
                self.close_client(client)
                self.send_to_all({
                    "type": "users_list",
                    "list": self._users_list
                })
            elif pkg["action"] == "get_users_list":
                client.send_pkg({
                    "type": "users_list",
                    "list": self._users_list
                })

    def handle_connexion(self, client, pkg):
        if len(self._connectedClients) < self._maxListen:
            if "action" in pkg and pkg["action"] == "connexion":
                if "pseudo" in pkg and pkg["pseudo"] not in self._clientByPseudo.keys():
                    token = str(uuid.uuid4())
                    self._clientByPseudo[pkg["pseudo"]] = client
                    client.set_pseudo(pkg["pseudo"])
                    client.set_token(token)
                    i = len(self._connectedClients)
                    if 0 <= i < 4:
                        self._users_list[i] = pkg["pseudo"]
                    if client.get_socket() in self._newClients:
                        self._newClients.remove(client.get_socket())
                    self._connectedClients.append(client.get_socket())
                    client.send_pkg({"connected": True, "token": token})
                    self.send_to_all({
                        "type": "users_list",
                        "list": self._users_list
                    })
                    if self._handler:
                        self._handler.player_connected(client)
                    return True
                else:
                    client.send_pkg({
                        "connected": False,
                        "error": "Pseudo already taken"
                    })
            else:
                client.send_pkg({
                    "connected": False,
                    "error": "Action should be connexion"
                })
        else:
            client.send_pkg({
                "connected": False,
                "error": "Server is full"
            })
