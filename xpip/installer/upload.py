#!/usr/bin/python3
# coding=utf-8

from argparse import ArgumentParser
import sys
from typing import List
from typing import Optional

from argcomplete import autocomplete
from twine.commands.check import main as check
from twine.commands.upload import main as upload

from ..util import URL_PROG


def add_cmd(_arg: ArgumentParser):
    _arg.add_argument("-d", "--debug", action="store_true",
                      help="show debug information")
    _arg.add_argument("--no-check", action="store_true",)
    _arg.add_argument("--only-check", action="store_true",)
    _arg.add_argument("dists", nargs="+",
                      help="The distribution files to upload.")


def run_cmd(args) -> int:
    if hasattr(args, "debug") and args.debug:
        for f in args.dists:
            sys.stdout.write(f"{f}\n")
        sys.stdout.flush()
    if not args.no_check:
        check(args.dists)
    if not args.only_check:
        upload(args.dists)
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    _arg = ArgumentParser(prog="xpip-upload",
                          description="upload python package",
                          epilog=f"For more, please visit {URL_PROG}")
    add_cmd(_arg)
    autocomplete(_arg)
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
