# coding=utf-8

import os
from typing import Any
from typing import Dict
from typing import List

from ping3 import ping
import toml

from .attribute import __author__
from .attribute import __author_email__
from .attribute import __description__
from .attribute import __project__
from .attribute import __url_bugs__
from .attribute import __url_code__
from .attribute import __url_docs__
from .attribute import __url_home__
from .attribute import __version__

DIR_CONF = f"{os.path.dirname(__file__)}/config"


def toml_load(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return toml.load(f)


def toml_dump(path: str, object: Dict[str, Any]) -> str:
    with open(path, "w") as f:
        return toml.dump(object, f)


def ping_second(address: str, count: int = 3, timeout: int = 1) -> float:
    delay: List[float] = []

    if count < 1:
        count = 1

    if timeout < 1:
        timeout = 1

    for i in range(count):
        t = ping(address, seq=i, timeout=timeout)
        # False on error and None on timeout.
        if t is None:
            return float(-timeout)
        if t is False:
            return 0.0
        delay.append(t)

    return sum(delay) / len(delay)
