# coding=utf-8

from argparse import ArgumentParser
from argparse import Namespace
import platform
import sys
from typing import List
from typing import Optional

from argcomplete import autocomplete
from pip import __version__ as pip_version

from .utils import __url_home__
from .utils import __version__ as xpip_version


def add_cmd(_arg: ArgumentParser):
    # _arg.add_argument("-d", "--debug", action="store_true",
    #                   help="show debug information")
    pass


def run_cmd(args: Namespace) -> int:
    python_version = f"python {platform.python_version()}, pip {pip_version}"
    sys.stderr.write(f"xpip {xpip_version} ({python_version})\n")
    sys.stdout.flush()
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    _arg = ArgumentParser(prog="xpip-version", description="show version",
                          epilog=f"For more, please visit {__url_home__}")
    add_cmd(_arg)
    autocomplete(_arg)
    args = _arg.parse_args(argv)

    # if hasattr(args, "debug") and args.debug:
    #     sys.stdout.write(f"{args}\n")
    #     sys.stdout.flush()

    try:
        return run_cmd(args)
    except KeyboardInterrupt:
        return 0
    # except BaseException as e:
    #     # if hasattr(args, "debug") and args.debug:
    #     #     raise e
    #     sys.stderr.write(f"{e}\n")
    #     sys.stderr.flush()
    #     return 10000
