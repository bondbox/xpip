# coding=utf-8

import os

from setuptools import find_packages
from setuptools import setup

from xpip_build.attribute import __author__
from xpip_build.attribute import __author_email__
from xpip_build.attribute import __description__
from xpip_build.attribute import __project__
from xpip_build.attribute import __urlbugs__
from xpip_build.attribute import __urlcode__
from xpip_build.attribute import __urldocs__
from xpip_build.attribute import __urlhome__
from xpip_build.attribute import __version__
from xpip_upload.attribute import __version__ as upload_version

long_description: str = os.path.join("docs", "xpip-build.md")

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
    packages=find_packages(include=["xpip_build*"]),
    install_requires=[f"xpip-upload >= {upload_version}",
                      "setuptools >= 69.3.0, <= 70.3.0"],
    entry_points={"console_scripts": ["xpip-build = xpip_build.cmds:main",]},
)
