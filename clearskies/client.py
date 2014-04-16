from clearskies.transport import UnixJsonTransport, WindowsJsonTransport
from clearskies.exc import ProtocolException, TransportException
import os
import platform

try:
    import xdg.BaseDirectory as xdgBaseDirectory
except ImportError:  # pragma: no cover
    # hack for dependency-free quickstart
    print("WARNING: failed to import xdg library, using hacky fallback")
    class xdgBaseDirectory:
        @staticmethod
        def save_data_path(x):
            path = os.path.join(os.path.expanduser("~/.local/share/"), x)
            if not os.path.exists(path):
                os.mkdir(path)
            return path


class ClearSkies(object):
    def __init__(self):
        data_dir = xdgBaseDirectory.save_data_path("clearskies")
        control_path = os.path.join(data_dir, "control")
        self.connected = False

        plat = platform.platform()
        if "Windows" in plat:
            self.socket = WindowsJsonTransport(control_path)
        else:
            self.socket = UnixJsonTransport(control_path)

    def connect(self):
        try:
            self.socket.connect()

            handshake = self.socket.recv()
            if handshake["protocol"] != 1:
                raise ValueError("Only protocol V1 is currently supported")

            self.connected = True
        except ValueError as e:
            raise ProtocolException("Error in CS handshake: %s" % e)

    def _cmd(self, cmd):
        try:
            self.socket.send(cmd)
            return self.socket.recv()
        except TransportException as e:
            self.connected = False
            raise

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
        })["shares"]

    def create_access_code(self, path, mode):
        valid_modes = ["read_write", "read_only", "untrusted"]
        if mode not in valid_modes:
            raise ValueError("Invalid access code mode, must be one of %s" % valid_modes)

        return self._cmd({
            "type": "create_access_code",
            "path": path,
            "mode": mode,
        })["access_code"]

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
