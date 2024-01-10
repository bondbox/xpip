# coding=utf-8

import setuptools

from xpip.utils import __author__
from xpip.utils import __author_email__
from xpip.utils import __description__
from xpip.utils import __name__
from xpip.utils import __url_bugs__
from xpip.utils import __url_code__
from xpip.utils import __url_docs__
from xpip.utils import __url_home__
from xpip.utils import __version__

setuptools.setup(
    name=__name__,
    version=__version__,
    description=__description__,
    url=__url_home__,
    author=__author__,
    author_email=__author_email__,
    project_urls={"Source Code": __url_code__,
                  "Bug Tracker": __url_bugs__,
                  "Documentation": __url_docs__})
