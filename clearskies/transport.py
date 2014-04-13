import socket
import json
import logging

from clearskies.exc import TransportException

log = logging.getLogger(__name__)


class Transport(object):
    def connect(self):
        raise NotImplementedError()

    def send(self, js):
        raise NotImplementedError()

    def recv(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()


class UnixJsonTransport(Transport):
    def __init__(self, control_path):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.control_path = control_path

    def connect(self):
        try:
            self.socket.connect(self.control_path)
        except socket.error as e:
            raise TransportException(e)

    def recv(self):
        try:
            data = self.socket.recv(1024)
            log.debug("< %s" % data)
            js = json.loads(data.decode("utf8"))
            return js
        except socket.error as e:
            raise TransportException(e)

    def send(self, js):
        try:
            log.debug("> %s" % js)
            data = json.dumps(js)
            self.socket.send((data + "\n").encode("utf8"))
        except socket.error as e:
            raise TransportException(e)

    def close(self):
        try:
            self.socket.close()
        except socket.error as e:
            raise TransportException(e)
