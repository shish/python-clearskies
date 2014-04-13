from mock import Mock, patch
import unittest2

from clearskies.unixjsonsocket import UnixJsonTransport


@patch("socket.socket")
class TestUnixJsonTransport(unittest2.TestCase):
    def test_init(self, socket):
        s = UnixJsonTransport("/")

    def test_connect(self, socket):
        s = UnixJsonTransport("foo.sock")
        s.connect()

        socket().connect.assert_called_with("foo.sock")

    def test_send(self, socket):
        s = UnixJsonTransport("foo.sock")
        s.connect()
        s.send({"foo": "bar"})

        socket().send.assert_called_with('{"foo": "bar"}\n')

    def test_recv(self, socket):
        s = UnixJsonTransport("foo.sock")
        s.connect()

        socket().recv.return_value = '{"foo": "bar"}'
        self.assertDictEqual(
            s.recv(),
            {"foo": "bar"}
        )

    def test_recv__not_json(self, socket):
        s = UnixJsonTransport("foo.sock")
        s.connect()

        socket().recv.return_value = 'somethingblah'
        self.assertRaises(ValueError, s.recv)

    def test_close(self, socket):
        s = UnixJsonTransport("foo.sock")
        s.connect()

        s.close()
        socket().close.assert_called_with()
