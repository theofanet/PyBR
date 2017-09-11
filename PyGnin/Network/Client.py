import socket
import json
from threading import Thread, RLock
import base64


class PkgHandler(object):
    def __init__(self, master=None):
        self._master = master

    def set_master(self, master):
        self._master = master

    def receive(self, data):
        pass

    def send(self, data):
        if self._master is not False:
            self._master.send_package(data)
        return self


class ClientRunThread(Thread):
    def __init__(self, cl):
        Thread.__init__(self)
        self._client = cl

    def run(self):
        while self._client.is_connected():
            with RLock():
                for received in self._client.receive_package():
                    if received is not False:
                        if "type" in received and received["type"] == "server_closing":
                            self._client.close(False, False)
                            return
                        else:
                            self._client.get_pkg_handler().receive(received)
                    else:
                        continue


class Client(object):
    def __init__(self, hostname="localhost", port=1234, pkg_handler=None):
        self._hostname = hostname
        self._port = port
        self._connected = False
        self._socketConnected = False
        self._connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connexion.settimeout(0.5)
        self._thread = ClientRunThread(self)
        self._pkgHandler = None
        self._last_error = "Unknown"
        self._token = ""
        if not pkg_handler:
            pkg_handler = PkgHandler()
        self.set_pkg_handler(pkg_handler)

    def get_last_error(self):
        return self._last_error

    def after_close(self):
        pass

    def get_token(self):
        return self._token

    def set_token(self, token):
        self._token = token

    def close(self, send_disconnect=True, join_thread=True):
        if self._socketConnected and send_disconnect:
            self.send_pkg({"action": "disconnect"})
        self._connected = False
        self._socketConnected = False
        if self._thread.isAlive() and join_thread:
            self._thread.abort = True
            self._thread.join()
            self._thread = ClientRunThread(self)
        self._connexion.close()
        self.after_close()

    def connect(self, pseudo, hostname=None, port=None):
        if not self._socketConnected:
            if self._hostname:
                self._hostname = hostname
            if self._port:
                self._port = port
            try:
                self._connexion.connect((self._hostname, self._port))
            except socket.timeout:
                self._connected = False
                self._last_error = "Unable to reach server"
                return False
            else:
                self._socketConnected = True

        return self._try_connect(pseudo)

    def is_connected(self):
        return self._connected

    def set_pkg_handler(self, handler):
        handler.set_master(self)
        self._pkgHandler = handler

    def get_pkg_handler(self):
        return self._pkgHandler

    def send_pkg(self, data):
        encoded_data = base64.b64encode(bytes(json.dumps(data) + "[END_BLOCK]", 'utf8'))
        self._connexion.send(encoded_data)

    def _try_connect(self, pseudo):
        encoded_data = base64.b64encode(bytes(json.dumps({
            "action": "connexion",
            "pseudo": pseudo
        }) + "[END_BLOCK]", 'utf8'))
        self._connexion.send(encoded_data)
        for response in self.receive_package():
            self._connected = False
            if 'connected' in response and response["connected"] and "token" in response:
                self._connected = True
                self._token = response["token"]
                return True
            elif "error" in response:
                self._last_error = response["error"]

        return False

    def receive_package(self):
        encoded_data = []
        decoded_data = []
        data = "DATABLOCK"
        #while len(data):
        try:
            data = self._connexion.recv(4096)
            if data:
                encoded_data.append(data.decode("utf8"))
        except socket.error as e:
            print(e)
            data = ""
            # continue
        if len(encoded_data):
            try:
                encoded_data = base64.b64decode(bytes("".join(encoded_data), 'utf8'))
                for json_data in encoded_data.decode("utf8").split("[END_BLOCK]"):
                    if json_data != '':
                        decoded_data.append(json.loads(json_data))
            except ValueError or TypeError as e:
                print("Unable to decode server message")
                print(e)

        return decoded_data

    def run(self):
        if self._connected:
            self._thread.start()
