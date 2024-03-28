# coding=utf-8

from setuptools import find_packages
from setuptools import setup

from xpip_build.util import __author__
from xpip_build.util import __author_email__
from xpip_build.util import __description__
from xpip_build.util import __project__
from xpip_build.util import __url_bugs__
from xpip_build.util import __url_code__
from xpip_build.util import __url_docs__
from xpip_build.util import __url_home__
from xpip_build.util import __version__
from xpip_upload.util import __version__ as upload_version

setup(
    name=__project__,
    version=__version__,
    description=__description__,
    keywords=["setuptools", "wheel"],
    url=__url_home__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __url_code__,
                  "Bug Tracker": __url_bugs__,
                  "Documentation": __url_docs__},
    packages=find_packages(include=["xpip_build*"]),
    install_requires=[f"xpip-upload >= {upload_version}",
                      "setuptools >= 51.0.0"],
    entry_points={"console_scripts": ["xpip-build = xpip_build.cmds:main",]},
)
