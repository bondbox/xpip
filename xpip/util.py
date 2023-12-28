# coding=utf-8

import os
from typing import List

from ping3 import ping
import toml

__version__ = "1.2.alpha.1"
URL_PROG = "https://github.com/bondbox/xpip-python"
DIR_CONF = f"{os.path.dirname(__file__)}/config"


def toml_load(path: str) -> dict:
    with open(path, "r") as f:
        return toml.load(f)


def toml_dump(path: str, object: dict) -> str:
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
