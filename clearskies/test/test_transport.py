from mock import patch
import unittest
import socket as _socket

from clearskies.exc import TransportException
from clearskies.transport import Transport, UnixJsonTransport, WindowsJsonTransport


class TestTransport(unittest.TestCase):
    def test_init(self):
        Transport("foo.sock")

    def test_connect(self):
        s = Transport("foo.sock")
        self.assertRaises(NotImplementedError, s.connect)

    def test_send(self):
        s = Transport("foo.sock")
        self.assertRaises(NotImplementedError, s.send, {})

    def test_recv(self):
        s = Transport("foo.sock")
        self.assertRaises(NotImplementedError, s.recv)

    def test_close(self):
        s = Transport("foo.sock")
        self.assertRaises(NotImplementedError, s.close)


@patch("socket.socket")
class TestUnixJsonTransport(unittest.TestCase):
    def test_init(self, socket):
        UnixJsonTransport("foo.sock")

    def test_connect(self, socket):
        s = UnixJsonTransport("foo.sock")
        s.connect()

        socket().connect.assert_called_with("foo.sock")

    def test_connect__error(self, socket):
        s = UnixJsonTransport("foo.sock")

        socket().connect.side_effect = _socket.error(2)
        self.assertRaises(TransportException, s.connect)

    def test_send(self, socket):
        s = UnixJsonTransport("foo.sock")
        s.connect()
        s.send({"foo": "bar"})

        socket().send.assert_called_with('{"foo": "bar"}\n'.encode("utf8"))

    def test_send__error(self, socket):
        s = UnixJsonTransport("foo.sock")
        s.connect()

        socket().send.side_effect = _socket.error(2)
        self.assertRaises(TransportException, s.send, {"foo": "bar"})

    def test_recv(self, socket):
        s = UnixJsonTransport("foo.sock")
        s.connect()

        socket().recv.return_value = '{"foo": "bar"}'.encode("utf8")
        self.assertDictEqual(
            s.recv(),
            {"foo": "bar"}
        )

    def test_recv__error(self, socket):
        s = UnixJsonTransport("foo.sock")
        s.connect()

        socket().recv.side_effect = _socket.error(2)
        self.assertRaises(TransportException, s.recv)

    def test_recv__not_json(self, socket):
        s = UnixJsonTransport("foo.sock")
        s.connect()

        socket().recv.return_value = 'somethingblah'.encode("utf8")
        self.assertRaises(TransportException, s.recv)

    def test_close(self, socket):
        s = UnixJsonTransport("foo.sock")
        s.connect()

        s.close()
        socket().close.assert_called_with()

    def test_close__error(self, socket):
        s = UnixJsonTransport("foo.sock")
        s.connect()

        socket().close.side_effect = _socket.error(2)
        self.assertRaises(TransportException, s.close)


@patch("clearskies.transport.win32file", None)
class TestWindowsJsonTransportImportError(unittest.TestCase):
    def test_init(self):
        WindowsJsonTransport("foo.sock")

    def test_connect__error(self):
        s = WindowsJsonTransport("foo.sock")

        self.assertRaises(TransportException, s.connect)


@patch("clearskies.transport.win32file")
class TestWindowsJsonTransport(unittest.TestCase):
    def test_init(self, win32file):
        WindowsJsonTransport("foo.sock")

    def test_connect(self, win32file):
        s = WindowsJsonTransport("foo.sock")
        s.connect()

        win32file.CreateFile.assert_called_with(
            "foo.sock",
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0, None,
            win32file.OPEN_EXISTING,
            0, None
        )

    def test_connect__error(self, win32file):
        s = WindowsJsonTransport("foo.sock")

        win32file.CreateFile.side_effect = Exception("I don't know what a real win32 exception looks like")
        self.assertRaises(TransportException, s.connect)

    def test_send(self, win32file):
        s = WindowsJsonTransport("foo.sock")
        s.connect()
        win32file.WriteFile.return_value = (0, 16)
        s.send({"foo": "bar"})

        win32file.WriteFile.assert_called_with(s.socket, '{"foo": "bar"}\n'.encode("utf8"))

    def test_send__error(self, win32file):
        s = WindowsJsonTransport("foo.sock")
        s.connect()

        win32file.WriteFile.return_value = (1, 0)
        self.assertRaises(TransportException, s.send, {"foo": "bar"})

        win32file.WriteFile.side_effect = Exception("I don't know what a real win32 exception looks like")
        self.assertRaises(TransportException, s.send, {"foo": "bar"})

    def test_recv(self, win32file):
        s = WindowsJsonTransport("foo.sock")
        s.connect()

        win32file.ReadFile.return_value = (0, '{"foo": "bar"}'.encode("utf8"))
        self.assertDictEqual(
            s.recv(),
            {"foo": "bar"}
        )

    def test_recv__error(self, win32file):
        s = WindowsJsonTransport("foo.sock")
        s.connect()

        win32file.ReadFile.return_value = (1, None)
        self.assertRaises(TransportException, s.recv)

        win32file.ReadFile.side_effect = Exception("I don't know what a real win32 exception looks like")
        self.assertRaises(TransportException, s.recv)

    def test_recv__not_json(self, win32file):
        s = WindowsJsonTransport("foo.sock")
        s.connect()

        win32file.ReadFile.return_value = (0, 'somethingblah'.encode("utf8"))
        self.assertRaises(TransportException, s.recv)

    def test_close(self, win32file):
        s = WindowsJsonTransport("foo.sock")
        s.connect()

        s.close()
        win32file.CloseHandle.assert_called_with(s.socket)

    def test_close__error(self, win32file):
        s = WindowsJsonTransport("foo.sock")
        s.connect()

        win32file.CloseHandle.side_effect = Exception("I don't know what a real win32 exception looks like")
        self.assertRaises(TransportException, s.close)
