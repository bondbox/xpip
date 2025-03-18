# coding=utf-8

import os

from setuptools import find_packages
from setuptools import setup

from xpip_upload.attribute import __author__
from xpip_upload.attribute import __author_email__
from xpip_upload.attribute import __description__
from xpip_upload.attribute import __project__
from xpip_upload.attribute import __urlbugs__
from xpip_upload.attribute import __urlcode__
from xpip_upload.attribute import __urldocs__
from xpip_upload.attribute import __urlhome__
from xpip_upload.attribute import __version__

long_description: str = os.path.join("docs", "xpip-upload.md")

setup(
    name=__project__,
    version=__version__,
    description=__description__,
    long_description=open(long_description).read(),
    long_description_content_type="text/markdown",
    keywords=["twine", "wheel"],
    url=__urlhome__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __urlcode__,
                  "Bug Tracker": __urlbugs__,
                  "Documentation": __urldocs__},
    packages=find_packages(include=["xpip_upload*"]),
    install_requires=["wheel", "packaging>=24.2", "twine>=6.1.0", "keyring", "keyrings.alt"],  # noqa:E501
    entry_points={"console_scripts": ["xpip-upload = xpip_upload.cmds:main"]},
)
