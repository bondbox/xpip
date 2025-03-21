# coding:utf-8

import unittest
from unittest import mock

from xpip_build import cmds
from xpip_build.cmds import setuptools


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

    def test_version(self):
        self.assertEqual(cmds.main(["--debug", "version"]), 0)

    def test_setup_clean(self):
        self.assertEqual(cmds.main(["--debug", "setup", "--file", "setup-upload.py", "--clean"]), 0)  # noqa:E501

    def test_setup_check(self):
        self.assertEqual(cmds.main(["--debug", "setup", "--file", "setup-upload.py", "--check"]), 0)  # noqa:E501

    def test_setup_all(self):
        self.assertEqual(cmds.main(["--debug", "setup", "--file", "setup-upload.py", "--all"]), 0)  # noqa:E501

    @mock.patch.object(setuptools, "run")
    def test_setup_install_debug(self, mock_run):
        mock_run.side_effect = [Exception()]
        self.assertRaises(Exception, cmds.main, ["--debug", "setup", "--file", "setup-upload.py", "--install"])  # noqa:E501,H202

    @mock.patch.object(setuptools, "run")
    def test_setup_install_KeyboardInterrupt(self, mock_run):
        mock_run.side_effect = [KeyboardInterrupt()]
        self.assertEqual(cmds.main(["--debug", "setup", "--file", "setup-upload.py", "--install"]), 0)  # noqa:E501

    @mock.patch.object(setuptools, "run")
    def test_setup_install(self, mock_run):
        mock_run.side_effect = [Exception()]
        self.assertEqual(cmds.main(["setup", "--file", "setup-upload.py", "--install"]), 10000)  # noqa:E501

    def test_setup_run(self):
        with mock.patch.object(setuptools.setuptools, "setup"):
            self.assertEqual(setuptools.run(setuptools.Namespace()), 0)

    def test_sub(self):
        self.assertEqual(cmds.main([]), cmds.ENOENT)


if __name__ == "__main__":
    unittest.main()
