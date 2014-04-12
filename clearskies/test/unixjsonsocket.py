from mock import Mock, patch
import unittest2

from clearskies.unixjsonsocket import UnixJsonSocket


@patch("socket.socket")
class TestUnixJsonSocket(unittest2.TestCase):
    def test_init(self, socket):
        s = UnixJsonSocket("/")

    def test_connect(self, socket):
        s = UnixJsonSocket("foo.sock")
        s.connect()

        socket().connect.assert_called_with("foo.sock")

    def test_send(self, socket):
        s = UnixJsonSocket("foo.sock")
        s.connect()
        s.send({"foo": "bar"})

        socket().send.assert_called_with('{"foo": "bar"}\n')

    def test_recv(self, socket):
        s = UnixJsonSocket("foo.sock")
        s.connect()

        socket().recv.return_value = '{"foo": "bar"}'
        self.assertDictEqual(
            s.recv(),
            {"foo": "bar"}
        )

    def test_recv__not_json(self, socket):
        s = UnixJsonSocket("foo.sock")
        s.connect()

        socket().recv.return_value = 'somethingblah'
        self.assertRaises(ValueError, s.recv)

    def test_close(self, socket):
        s = UnixJsonSocket("foo.sock")
        s.connect()

        s.close()
        socket().close.assert_called_with()