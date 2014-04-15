import socket
import json
import logging

from clearskies.exc import TransportException

log = logging.getLogger(__name__)


class Transport(object):  # pragma: no cover
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
        self.socket = None
        self.control_path = control_path

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.socket.connect(self.control_path)
        except socket.error as e:
            raise TransportException(e)

    def recv(self):
        try:
            data = self.socket.recv(1024)
            log.debug("< %s" % data.strip())
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


try:
    import win32file
    import win32pipe
    have_win32 = True
except ImportError:
    have_win32 = False


class WindowsJsonTransport(Transport):
    def __init__(self, control_path):
        self.socket = None
        self.control_path = control_path

    def connect(self):
        try:
            if not have_win32:
                raise TransportException("Error importing win32file / win32pipe modules")

            self.socket = win32file.CreateFile(
                self.control_path,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0, None,
                win32file.OPEN_EXISTING,
                0, None
            )
        except Exception as e:
            raise TransportException(e)

    def recv(self):
        try:
            status, data = win32file.ReadFile(self.socket, 4096)
            if status != 0:
                raise Exception("Error %d" % status)
            log.debug("< %s" % data.strip())
            js = json.loads(data.decode("utf8"))
            return js
        except Exception as e:
            raise TransportException("Error while reading from socket: %s" % e)

    def send(self, js):
        try:
            log.debug("> %s" % js)
            data = json.dumps(js)
            status, bytes_written = win32file.WriteFile(self.socket, (data + "\n").encode("utf8"))
            if status != 0:
                raise Exception("Error %d" % status)
        except Exception as e:
            raise TransportException("Error while writing to socket: %s" % e)

    def close(self):
        try:
            win32file.CloseHandle(self.socket)
        except Exception as e:
            raise TransportException("Error while closing socket: %s" % e)
