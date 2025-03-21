# coding:utf-8

import unittest
from unittest import mock

from xpip_mirror import util


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

    @mock.patch.object(util, "ping")
    def test_ping_second_none(self, mock_ping):
        mock_ping.side_effect = [None]
        self.assertEqual(util.ping_second("example.com"), -1.0)

    @mock.patch.object(util, "ping")
    def test_ping_second_false(self, mock_ping):
        mock_ping.side_effect = [False]
        self.assertEqual(util.ping_second("example.com"), 0.0)

    @mock.patch.object(util, "ping")
    def test_ping_second(self, mock_ping):
        mock_ping.side_effect = [1.0, 2.0, 3.0]
        self.assertEqual(util.ping_second("example.com"), 2.0)


if __name__ == "__main__":
    unittest.main()
