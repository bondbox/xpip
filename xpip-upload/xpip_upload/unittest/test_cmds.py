# coding:utf-8

import unittest
from unittest import mock

from xpip_upload import cmds


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

    @mock.patch.object(cmds, "run_cmd")
    def test_KeyboardInterrupt(self, mock_run_cmd):
        mock_run_cmd.side_effect = [KeyboardInterrupt()]
        self.assertEqual(cmds.main(["--debug", "test"]), 0)

    @mock.patch.object(cmds, "run_cmd")
    def test_BaseException_raise(self, mock_run_cmd):
        mock_run_cmd.side_effect = [Exception()]
        self.assertRaises(Exception, cmds.main, ["--debug", "test"])  # noqa:E501,H202

    @mock.patch.object(cmds, "run_cmd")
    def test_BaseException(self, mock_run_cmd):
        mock_run_cmd.side_effect = [Exception()]
        self.assertEqual(cmds.main(["test"]), 10000)

    @mock.patch.object(cmds.os.path, "isfile")
    @mock.patch.object(cmds, "check", mock.MagicMock())
    @mock.patch.object(cmds, "upload", mock.MagicMock())
    @mock.patch.object(cmds, "get_project_name", mock.MagicMock(return_value="test"))  # noqa:E501
    def test_run_cmd_token(self, mock_isfile):
        mock_isfile.return_value = True
        self.assertEqual(cmds.main(["--debug", "--verbose", "--token", "demo", "test.whl"]), 0)  # noqa:E501

    @mock.patch.object(cmds.os.path, "isfile")
    @mock.patch.object(cmds, "check", mock.MagicMock())
    @mock.patch.object(cmds, "upload", mock.MagicMock())
    @mock.patch.object(cmds, "get_project_name", mock.MagicMock(return_value="test"))  # noqa:E501
    def test_run_cmd(self, mock_isfile):
        mock_isfile.return_value = True
        self.assertEqual(cmds.main(["--debug", "--verbose",
                                    "--repository", "pypi",
                                    "--repository-url", "url",
                                    "test.whl"]), 0)

    @mock.patch.object(cmds.PackageFile, "from_filename")
    def test_get_project_name(self, mock_pkgf):
        fake_meta = mock.MagicMock()
        fake_meta.get.side_effect = ["test"]
        fake_pkgf = mock.MagicMock()
        fake_pkgf.metadata_dictionary.side_effect = [fake_meta]
        mock_pkgf.side_effect = [fake_pkgf]
        self.assertEqual(cmds.get_project_name("test.whl"), "test")


if __name__ == "__main__":
    unittest.main()
