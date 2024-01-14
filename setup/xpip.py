# coding=utf-8

from setuptools import find_packages
from setuptools import setup

from xpip.utils import __author__
from xpip.utils import __author_email__
from xpip.utils import __description__
from xpip.utils import __name__
from xpip.utils import __url_bugs__
from xpip.utils import __url_code__
from xpip.utils import __url_docs__
from xpip.utils import __url_home__
from xpip.utils import __version__

setup(
    name=__name__,
    version=__version__,
    description=__description__,
    keywords=["setuptools", "wheel", "twine"],
    url=__url_home__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __url_code__,
                  "Bug Tracker": __url_bugs__,
                  "Documentation": __url_docs__},
    packages=find_packages(include=["xpip*"], exclude=["xpip_mirror*"]),
    install_requires=["argcomplete", "tabulate", "setuptools >= 51.0.0",
                      "wheel", "twine", "keyring", "keyrings.alt",
                      "xpip-mirror"],
    entry_points={"console_scripts": [
        "xpip-version = xpip.version:main",
        "xpip-build = xpip.builder.build:main",
        "xpip-upload = xpip.installer.upload:main"]},
)
