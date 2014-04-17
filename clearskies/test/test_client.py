from mock import patch, Mock
import unittest
import sys

from clearskies.client import ClearSkies, ProtocolException
from clearskies.exc import TransportException


_open = "__builtin__.open" if sys.version_info[0] == 2 else "builtins.open"


# This one test needs a controllable mock of platform.platform()
# Every other test can use a constant of Linux to force UJS
class TestClearSkies_Init(unittest.TestCase):
    @patch("clearskies.client.UnixJsonTransport")
    @patch("clearskies.client.WindowsJsonTransport")
    @patch("platform.platform")
    def test_init(self, platform, WJS, UJS):
        platform.return_value = "Windows"
        c = ClearSkies()
        self.assertEqual(c.socket, WJS())

        platform.return_value = "Linux"
        c = ClearSkies()
        self.assertEqual(c.socket, UJS())


@patch("platform.platform", Mock(return_value="Linux"))
@patch("clearskies.client.UnixJsonTransport")
class TestClearSkies(unittest.TestCase):
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

    ##########################################################################
    # Not official APIs section
    ##########################################################################
    def test_get_log_data(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            # get_log_data bypasses the server and gets data straight from the file
            # possibly this should change in future
        ]

        c = ClearSkies()
        c.connect()

        with patch(_open) as mock_open:
            mock_open.return_value.read.return_value = "some\nlog\ndata\n"
            # get all the log data
            self.assertEqual(c.get_log_data(), "some\nlog\ndata\n")

            # get the bottom two lines
            self.assertEqual(c.get_log_data(2), "log\ndata\n")

    def test_get_log_data__io_error(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            # get_log_data bypasses the server and gets data straight from the file
            # possibly this should change in future
        ]

        c = ClearSkies()
        c.connect()

        with patch(_open) as mock_open:
            mock_open.side_effect = IOError("File not found")
            self.assertRaises(ProtocolException, c.get_log_data)

    def test_get_config(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {"config": {"key": "value"}},
        ]

        c = ClearSkies()
        c.connect()
        c.set_config({"key": "value"})  # hack
        self.assertDictEqual(
            c.get_config(),
            {"key": "value"}
        )

        #UJS().send.assert_called_with({
        #    "type": "get_config",
        #})

    def test_set_config(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {},
        ]

        c = ClearSkies()
        c.connect()
        c.set_config({"key": "value"})

        #UJS().send.assert_called_with({
        #    "type": "set_config",
        #    "config": {"key": "value"},
        #})

    def test_get_config_value(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {"value": "bar"},
        ]

        c = ClearSkies()
        c.connect()
        c.set_config({"foo": "bar"})  # hack
        self.assertEqual(
            c.get_config_value("foo"),
            "bar"
        )

        #UJS().send.assert_called_with({
        #    "type": "get_config_value",
        #    "key": "foo",
        #})

    def test_set_config_value(self, UJS):
        UJS().recv.side_effect = [
            {"protocol": 1, "service": "ClearSkies Control", "software": "test"},
            {},
        ]

        c = ClearSkies()
        c.connect()
        c.set_config_value("foo", "bar")

        #UJS().send.assert_called_with({
        #    "type": "set_config_value",
        #    "key": "foo",
        #    "value": "bar",
        #})
