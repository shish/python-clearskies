from clearskies.unixjsonsocket import UnixJsonSocket
import xdg.BaseDirectory
import os


class ProtocolException(Exception):
    pass


class ClearSkies(object):
    def __init__(self):
        data_dir = xdg.BaseDirectory.save_data_path("clearskies")
        control_path = os.path.join(data_dir, "control")
        self.socket = UnixJsonSocket(control_path)

    def connect(self):
        self.socket.connect()

        try:
            handshake = self.socket.recv()
            if handshake["protocol"] != 1:
                raise ValueError("Only protocol V1 is currently supported")
        except ValueError as e:
            raise ProtocolException("Error in CS handshake: %s" % e)

    def _cmd(self, cmd):
        try:
            self.socket.send(cmd)
            return self.socket.recv()
        except ValueError as e:
            raise ProtocolException("Error decoding command: %s" % e)

    def stop(self):
        return self._cmd({
            "type": "stop",
        })

    def pause(self):
        return self._cmd({
            "type": "pause",
        })

    def resume(self):
        return self._cmd({
            "type": "resume",
        })

    def status(self):
        return self._cmd({
            "type": "status",
        })

    def create_share(self, path):
        return self._cmd({
            "type": "create_share",
            "path": path,
        })

    def list_shares(self):
        return self._cmd({
            "type": "list_shares",
        })

    def create_access_code(self, path, mode):
        return self._cmd({
            "type": "create_access_code",
            "path": path,
            "mode": mode,
        })

    def add_share(self, code, path):
        return self._cmd({
            "type": "add_share",
            "code": code,
            "path": path,
        })

    def remove_share(self, path):
        return self._cmd({
            "type": "remove_share",
            "path": path,
        })
