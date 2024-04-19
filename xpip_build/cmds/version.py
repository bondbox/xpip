# coding=utf-8

from argparse import ArgumentParser
from argparse import Namespace
import platform
import sys
from typing import List

from setuptools import __version__ as setuptools_version

from ..attribute import __version__ as xpip_version


def add_cmd(_arg: ArgumentParser):
    pass


def run_cmd(args: Namespace) -> int:
    versions: List[str] = [f"python {platform.python_version()}",
                           f"setuptools {setuptools_version}"]
    sys.stderr.write(f"xpip-build {xpip_version} ({', '.join(versions)})\n")
    sys.stdout.flush()
    return 0
