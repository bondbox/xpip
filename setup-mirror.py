# coding=utf-8

import os

from setuptools import find_packages
from setuptools import setup

from xpip_mirror.util import __author__
from xpip_mirror.util import __author_email__
from xpip_mirror.util import __description__
from xpip_mirror.util import __project__
from xpip_mirror.util import __url_bugs__
from xpip_mirror.util import __url_code__
from xpip_mirror.util import __url_docs__
from xpip_mirror.util import __url_home__
from xpip_mirror.util import __version__

long_description: str = os.path.join("docs", "xpip-mirror.md")

setup(
    name=__project__,
    version=__version__,
    description=__description__,
    long_description=open(long_description).read(),
    long_description_content_type="text/markdown",
    keywords=["pip", "pypi", "mirror"],
    python_requires=">=3.8",
    url=__url_home__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __url_code__,
                  "Bug Tracker": __url_bugs__,
                  "Documentation": __url_docs__},
    packages=find_packages(include=["xpip_mirror*"]),
    package_data={"xpip_mirror.config": ["mirrors.toml"]},
    install_requires=["xarg-python >= 1.4.3", "tabulate", "wcwidth",
                      "pip", "toml", "ping3"],
    entry_points={"console_scripts": ["xpip-mirror = xpip_mirror.cmds:main"]},
)
