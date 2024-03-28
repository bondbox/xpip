# coding=utf-8

from setuptools import find_packages
from setuptools import setup

from xpip_upload.util import __author__
from xpip_upload.util import __author_email__
from xpip_upload.util import __description__
from xpip_upload.util import __project__
from xpip_upload.util import __url_bugs__
from xpip_upload.util import __url_code__
from xpip_upload.util import __url_docs__
from xpip_upload.util import __url_home__
from xpip_upload.util import __version__

setup(
    name=__project__,
    version=__version__,
    description=__description__,
    keywords=["twine", "wheel"],
    url=__url_home__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __url_code__,
                  "Bug Tracker": __url_bugs__,
                  "Documentation": __url_docs__},
    packages=find_packages(include=["xpip_upload*"]),
    install_requires=["wheel", "twine", "keyring", "keyrings.alt"],
    entry_points={"console_scripts": ["xpip-upload = xpip_upload.cmds:main"]},
)
