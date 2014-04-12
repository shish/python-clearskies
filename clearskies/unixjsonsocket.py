import socket
import json


class UnixJsonSocket(object):
    def __init__(self, control_path):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.control_path = control_path
        self.debug = False

    def connect(self):
        self.socket.connect(self.control_path)

    def recv(self):
        data = self.socket.recv(1024)
        js = json.loads(data.decode("utf8"))
        if self.debug:
            print("< %s" % js)
        return js

    def send(self, js):
        if self.debug:
            print("> %s" % js)
        data = json.dumps(js)
        self.socket.send(data+"\n")

    def close(self):
        self.socket.close()
