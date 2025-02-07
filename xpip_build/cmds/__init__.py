# coding=utf-8

from argparse import ArgumentParser
from argparse import Namespace
from errno import ENOENT
import os
import sys
from typing import List
from typing import Optional

from ..attribute import __description__
from ..attribute import __urlhome__
from .setuptools import add_cmd as add_cmd_setup
from .setuptools import run_cmd as run_cmd_setup
from .version import add_cmd as add_cmd_version
from .version import run_cmd as run_cmd_version

try:
    from argcomplete import autocomplete
except ModuleNotFoundError:
    pass

EPILOG = f"For more, please visit {__urlhome__}"


def add_cmd(_arg: ArgumentParser):
    _arg.add_argument("-d", "--debug", action="store_true",
                      help="show debug information")
    _arg.add_argument("--path", nargs="?", type=str, const=".", default=".",
                      help="specify root path, default current directory")
    _sub = _arg.add_subparsers(dest="sub_build")
    add_cmd_setup(_sub.add_parser("setup", help="build based on setuptools",
                                  description="build package via setuptools",
                                  epilog=EPILOG))
    add_cmd_version(_sub.add_parser("version", help="show version",
                                    description="show version",
                                    epilog=EPILOG))


def run_cmd(args: Namespace) -> int:
    cmds = {
        "setup": run_cmd_setup,
        "version": run_cmd_version,
    }
    if not hasattr(args, "sub_build") or args.sub_build not in cmds:
        return ENOENT
    args.root = os.path.realpath(args.path)
    if hasattr(args, "debug") and args.debug:
        sys.stdout.write(f"root: {args.root}\n")
        sys.stdout.flush()
    return cmds[args.sub_build](args)


def main(argv: Optional[List[str]] = None) -> int:
    _arg = ArgumentParser(prog="xpip-build", description=__description__,
                          epilog=EPILOG)
    add_cmd(_arg)

    try:
        autocomplete(_arg)
    except NameError:
        pass

    args = _arg.parse_args(argv)

    if hasattr(args, "debug") and args.debug:
        sys.stdout.write(f"{args}\n")
        sys.stdout.flush()

    try:
        return run_cmd(args)
    except KeyboardInterrupt:
        return 0
    except BaseException as e:
        if hasattr(args, "debug") and args.debug:
            raise e
        sys.stderr.write(f"{e}\n")
        sys.stderr.flush()
        return 10000
