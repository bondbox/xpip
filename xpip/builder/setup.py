#!/usr/bin/python3
# coding=utf-8

from argparse import ArgumentParser
import glob
import os
import shutil
import sys

import setuptools


def run(args) -> int:
    if hasattr(args, "setup_py") and isinstance(args.setup_py, str):
        exec(args.setup_py)
    else:
        setuptools.setup()
    return 0


def check(args) -> int:
    sys.argv = "setup.py check".split()
    return run(args)


def sdist(args) -> int:
    sys.argv = "setup.py sdist".split()
    return run(args)


def bdist_wheel(args) -> int:
    sys.argv = "setup.py bdist_wheel --universal".split()
    return run(args)


def install(args) -> int:
    # TODO: uninstall
    sys.argv = "setup.py install".split()
    return run(args)


def clean(args) -> int:
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
    _arg.add_argument("--clean", action="store_true", help="clean build files")
    marg = _arg.add_mutually_exclusive_group()
    marg.add_argument("--check", action="store_true", help="build check")
    marg.add_argument("--sdist", action="store_true", help="build sdist")
    marg.add_argument("--bdist_wheel", action="store_true",
                      help="build bdist_wheel")
    marg.add_argument("--all", action="store_true",
                      help="build check and all distribution files")
    _arg.add_argument("--install", action="store_true",
                      help="install build package")


def run_cmd(args) -> int:
    os.chdir(args.root)

    if os.path.isfile("setup.py"):
        with open("setup.py", "r") as f:
            args.setup_py = f.read()
            if hasattr(args, "debug") and args.debug:
                sys.stdout.write(f"setup.py:\n{args.setup_py}\n")
                sys.stdout.flush()

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

    return 0
