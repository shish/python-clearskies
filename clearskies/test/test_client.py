from mock import Mock, patch
import unittest

from clearskies.client import ClearSkies, ProtocolException
from clearskies.exc import TransportException


@patch("clearskies.client.UnixJsonTransport")
class TestClearSkies(unittest.TestCase):
    @patch("clearskies.client.WindowsJsonTransport")
    @patch("platform.platform")
    def test_init(self, platform, WJS, UJS):
        platform.return_value = "Windows"
        c = ClearSkies()
        self.assertEqual(c.socket, WJS())

        platform.return_value = "Linux"
        c = ClearSkies()
        self.assertEqual(c.socket, UJS())

    def test_connect(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
        ]

        c = ClearSkies()
        c.connect()

    def test_connect__not_json(self, UJS):
        UJS().recv.side_effect = [
            ValueError("Could not decode JSON"),
        ]

        c = ClearSkies()
        self.assertRaises(ProtocolException, c.connect)

    def test_connect__bad_protocol(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 2, "service": "ClearSkies Control", "software": "test"}
        ]

        c = ClearSkies()
        self.assertRaises(ProtocolException, c.connect)

    def test_stop(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {},
        ]

        c = ClearSkies()
        c.connect()
        c.stop()

        UJS().send.assert_called_with({
            "type": "stop",
        })

    def test_stop__error(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            TransportException("Could not decode JSON"),
        ]

        c = ClearSkies()
        c.connect()
        self.assertRaises(TransportException, c.stop)

    def test_pause(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {},
        ]

        c = ClearSkies()
        c.connect()
        c.pause()

        UJS().send.assert_called_with({
            "type": "pause",
        })

    def test_resume(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {},
        ]

        c = ClearSkies()
        c.connect()
        c.resume()

        UJS().send.assert_called_with({
            "type": "resume",
        })

    def test_status(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {},
        ]

        c = ClearSkies()
        c.connect()
        c.status()

        UJS().send.assert_called_with({
            "type": "status",
        })

    def test_create_share(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {},
        ]

        c = ClearSkies()
        c.connect()
        c.create_share("/home/foo/Shared")

        UJS().send.assert_called_with({
            "type": "create_share",
            "path": "/home/foo/Shared",
        })

    def test_list_shares(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {"shares": [{"path": "/home/foo/Shared", "status": "N/A"}]},
        ]

        c = ClearSkies()
        c.connect()
        c.list_shares()

        UJS().send.assert_called_with({
            "type": "list_shares",
        })

    def test_create_access_code(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {"access_code": "SYNC123ABC"},
        ]

        c = ClearSkies()
        c.connect()
        code = c.create_access_code("/home/foo/Shared", "read_write")

        self.assertEqual(code, "SYNC123ABC")
        UJS().send.assert_called_with({
            "type": "create_access_code",
            "path": "/home/foo/Shared",
            "mode": "read_write",
        })

    def test_create_access_code__invalid_mode(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {},
        ]

        c = ClearSkies()
        c.connect()
        self.assertRaises(ValueError, c.create_access_code, "/home/foo/Shared", "not_a_real_mode")

    def test_add_share(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {},
        ]

        c = ClearSkies()
        c.connect()
        c.add_share("ABCDEF", "/home/foo/Shared")

        UJS().send.assert_called_with({
            "type": "add_share",
            "code": "ABCDEF",
            "path": "/home/foo/Shared",
        })

    def test_remove_share(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {},
        ]

        c = ClearSkies()
        c.connect()
        c.remove_share("/home/foo/Shared")

        UJS().send.assert_called_with({
            "type": "remove_share",
            "path": "/home/foo/Shared",
        })
