# coding=utf-8

import os
from os.path import dirname
from os.path import join
import sys
from urllib.parse import urljoin

from setuptools import find_packages
from setuptools import setup
from xpip_build.attribute import __author__
from xpip_build.attribute import __author_email__
from xpip_build.attribute import __description__
from xpip_build.attribute import __project__
from xpip_build.attribute import __urlhome__
from xpip_build.attribute import __version__

sys.path.insert(0, join(dirname(__file__), "..", "xpip-upload"))
from xpip_upload.attribute import __version__ as upload_version  # noqa:E402

__urlcode__ = __urlhome__
__urldocs__ = __urlhome__
__urlbugs__ = urljoin(__urlhome__, "issues")
long_description: str = os.path.join("..", "docs", "xpip-build.md")


def all_requirements():
    def read_requirements(path: str):
        with open(path, "r", encoding="utf-8") as rhdl:
            return rhdl.read().splitlines()

    requirements = read_requirements("requirements.txt")
    requirements.append(f"xpip-upload>={upload_version}")
    return requirements


setup(
    name=__project__,
    version=__version__,
    description=__description__,
    long_description=open(long_description).read(),
    long_description_content_type="text/markdown",
    keywords=["setuptools", "wheel"],
    url=__urlhome__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __urlcode__,
                  "Bug Tracker": __urlbugs__,
                  "Documentation": __urldocs__},
    packages=find_packages(include=["xpip_build*"],
                           exclude=["xpip_build.unittest"]),
    install_requires=all_requirements(),
    entry_points={"console_scripts": ["xpip-build = xpip_build.cmds:main",]},
)
