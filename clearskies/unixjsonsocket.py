import socket
import json
import logging

log = logging.getLogger(__name__)


class UnixJsonSocket(object):
    def __init__(self, control_path):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.control_path = control_path

    def connect(self):
        self.socket.connect(self.control_path)

    def recv(self):
        data = self.socket.recv(1024)
        log.debug("< %s" % data)
        js = json.loads(data.decode("utf8"))
        return js

    def send(self, js):
        data = json.dumps(js)
        log.debug("> %s" % data)
        self.socket.send(data+"\n")

    def close(self):
        self.socket.close()
