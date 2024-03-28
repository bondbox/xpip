# coding=utf-8

from argparse import ArgumentParser
from argparse import Namespace
import platform
import sys

from pip import __version__ as pip_version

from ..util import __version__ as xpip_version


def add_cmd(_arg: ArgumentParser):
    pass


def run_cmd(args: Namespace) -> int:
    python_version = f"python {platform.python_version()}, pip {pip_version}"
    sys.stderr.write(f"xpip-build {xpip_version} ({python_version})\n")
    sys.stdout.flush()
    return 0
