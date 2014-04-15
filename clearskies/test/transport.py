from mock import Mock, patch
import unittest
import socket as _socket

from clearskies.exc import TransportException
from clearskies.transport import UnixJsonTransport


@patch("socket.socket")
class TestUnixJsonTransport(unittest.TestCase):
    def test_init(self, socket):
        s = UnixJsonTransport("/")

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
        self.assertRaises(ValueError, s.recv)

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
