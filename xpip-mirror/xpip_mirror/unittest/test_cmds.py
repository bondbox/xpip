# coding:utf-8

import unittest
from unittest import mock

from xpip_mirror import cmds


class TestCmds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch.object(cmds, "choice_mirror")
    def test_list(self, mock_choice_mirror):
        mirror = cmds.MIRROR("demo", "url", "test", "unit", 1.0)
        mock_choice_mirror.side_effect = [mirror]
        self.assertEqual(cmds.main(["list"]), 0)

    def test_get(self):
        self.assertEqual(cmds.main(["get", "pypi"]), 0)

    def test_set(self):
        self.assertEqual(cmds.main(["set", "pypi", "https://pypi.org/simple"]), 0)  # noqa:E501

    def test_now(self):
        self.assertEqual(cmds.main(["now"]), 0)

    @mock.patch.object(cmds, "pipcli")
    @mock.patch.object(cmds, "choice_mirror")
    def test_choice_best(self, mock_choice_mirror, mock_pipcli):
        mock_pipcli.side_effect = [0]
        mirror = cmds.MIRROR("demo", "url", "test", "unit", 1.0)
        mock_choice_mirror.side_effect = [mirror]
        self.assertEqual(cmds.main(["choice"]), 0)

    def test_get_mirror_hostname_error(self):
        mirror = cmds.get_mirror("test", "unit")
        self.assertIsInstance(mirror, cmds.MIRROR)

    @mock.patch.object(cmds, "ping_second")
    def test_get_mirror_ping_error(self, mock_ping):
        mock_ping.side_effect = [cmds.socket.error()]
        mirror = cmds.get_mirror("test", "https://pypi.org/simple")
        self.assertIsInstance(mirror, cmds.MIRROR)

    def test_choice_mirror_hostname_error(self):
        mirror = cmds.MIRROR("demo", "url", "ERROR", "UNKOWN", 0.0)
        self.assertIsNone(cmds.choice_mirror([mirror], "demo"))

    def test_choice_mirror_address_unkown(self):
        mirror = cmds.MIRROR("demo", "url", "test", "UNKOWN", 0.0)
        self.assertIsNone(cmds.choice_mirror([mirror], "demo"))

    def test_choice_mirror_ping_timeout(self):
        mirror = cmds.MIRROR("demo", "url", "test", "unit", -1.0)
        self.assertIsNone(cmds.choice_mirror([mirror], "demo"))

    def test_choice_mirror(self):
        mirror = cmds.MIRROR("demo", "url", "test", "unit", 0.0)
        self.assertIs(cmds.choice_mirror([mirror], "demo"), mirror)

    def test_choice_mirror_best(self):
        mirror = cmds.MIRROR("demo", "url", "test", "unit", 1.0)
        self.assertIs(cmds.choice_mirror([mirror]), mirror)

    def test_choice_mirror_not_found(self):
        mirror = cmds.MIRROR("demo", "url", "test", "unit", 0.0)
        self.assertIsNone(cmds.choice_mirror([mirror], "test"))


if __name__ == "__main__":
    unittest.main()
