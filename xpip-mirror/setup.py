# coding=utf-8

import os
from urllib.parse import urljoin

from setuptools import find_packages
from setuptools import setup
from xpip_mirror.attribute import __author__
from xpip_mirror.attribute import __author_email__
from xpip_mirror.attribute import __description__
from xpip_mirror.attribute import __project__
from xpip_mirror.attribute import __urlhome__
from xpip_mirror.attribute import __version__

__urlcode__ = __urlhome__
__urldocs__ = __urlhome__
__urlbugs__ = urljoin(__urlhome__, "issues")
long_description: str = os.path.join("..", "docs", "xpip-mirror.md")


def all_requirements():
    def read_requirements(path: str):
        with open(path, "r", encoding="utf-8") as rhdl:
            return rhdl.read().splitlines()

    requirements = read_requirements("requirements.txt")
    return requirements


setup(
    name=__project__,
    version=__version__,
    description=__description__,
    long_description=open(long_description).read(),
    long_description_content_type="text/markdown",
    keywords=["pip", "pypi", "mirror"],
    python_requires=">=3.8",
    url=__urlhome__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __urlcode__,
                  "Bug Tracker": __urlbugs__,
                  "Documentation": __urldocs__},
    packages=find_packages(include=["xpip_mirror*"],
                           exclude=["xpip_mirror.unittest"]),
    package_data={"xpip_mirror.config": ["mirrors.toml"]},
    install_requires=all_requirements(),
    entry_points={"console_scripts": ["xpip-mirror = xpip_mirror.cmds:main"]},
)
