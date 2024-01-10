# coding=utf-8

from argparse import ArgumentParser
from argparse import Namespace
import glob
import os
import shutil
import sys
from types import CodeType

import setuptools


def run(args: Namespace) -> int:
    if hasattr(args, "setup_code") and isinstance(args.setup_code, CodeType):
        exec(args.setup_code)
    else:
        setuptools.setup()
    return 0


def check(args: Namespace) -> int:
    sys.argv = "setup.py check".split()
    return run(args)


def sdist(args: Namespace) -> int:
    sys.argv = "setup.py sdist".split()
    return run(args)


def bdist_wheel(args: Namespace) -> int:
    sys.argv = "setup.py bdist_wheel --universal".split()
    return run(args)


def install(args: Namespace) -> int:
    # TODO: uninstall
    sys.argv = "setup.py install".split()
    return run(args)


def clean(args: Namespace) -> int:
    to_delete_dirs = []
    to_delete_dirs.extend(glob.glob("build"))
    to_delete_dirs.extend(glob.glob("dist"))
    to_delete_dirs.extend(glob.glob("*.egg-info"))

    # delete build/dist/*.egg-info directorys
    for dir in to_delete_dirs:
        if os.path.isdir(dir):
            if hasattr(args, "debug") and args.debug:
                sys.stdout.write(f"delete directory: {dir}\n")
                sys.stdout.flush()
            shutil.rmtree(dir)

    # TODO: delete *.pyc and *.pyo
    to_delete_files = []
    to_delete_files.extend(
        glob.glob(os.path.join("**", "*.pyc"), recursive=True))
    to_delete_files.extend(
        glob.glob(os.path.join("**", "*.pyo"), recursive=True))

    for file in to_delete_files:
        if os.path.isfile(file):
            if hasattr(args, "debug") and args.debug:
                sys.stdout.write(f"delete file: {file}\n")
                sys.stdout.flush()
            os.remove(file)

    return 0


def add_cmd(_arg: ArgumentParser):
    _arg.add_argument("--clean", action="store_true",
                      help="clean files before build")
    marg = _arg.add_mutually_exclusive_group()
    marg.add_argument("--check", action="store_true", help="build check")
    marg.add_argument("--sdist", action="store_true", help="build sdist")
    marg.add_argument("--bdist_wheel", action="store_true",
                      help="build bdist_wheel")
    marg.add_argument("--all", action="store_true",
                      help="build check and all distribution files")
    _arg.add_argument("--install", action="store_true",
                      help="install package after build")


def run_cmd(args: Namespace) -> int:
    cwd = os.getcwd()
    os.chdir(args.root)

    if os.path.isfile("setup.py"):
        with open("setup.py", "r") as f:
            sys.path.insert(0, args.root)
            code = compile(f.read(), "setup.py", "exec")
            if hasattr(args, "debug") and args.debug:
                sys.stdout.write(f"co_name: {code.co_name}\n")
                sys.stdout.write(f"co_names: {code.co_names}\n")
                sys.stdout.write(f"co_filename: {code.co_filename}\n")
                sys.stdout.flush()
            args.setup_code = code

    if args.clean:
        clean(args)

    if args.all or args.check:
        check(args)

    if args.all or args.sdist:
        sdist(args)

    if args.all or args.bdist_wheel:
        bdist_wheel(args)

    if args.install:
        install(args)

    os.chdir(cwd)
    return 0
