# coding=utf-8

import os
from typing import Any
from typing import Dict
from typing import List

from ping3 import ping
import toml

DIR_CONF = f"{os.path.dirname(__file__)}/config"


def toml_load(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return toml.load(f)


def toml_dump(path: str, obj: Dict[str, Any]) -> str:
    with open(path, "w", encoding="utf-8") as f:
        return toml.dump(obj, f)


def ping_second(address: str, count: int = 3, timeout: int = 1) -> float:
    delay: List[float] = []
    count = max(1, count)
    timeout = max(1, timeout)

    for i in range(count):
        t = ping(address, seq=i, timeout=timeout)
        # False on error and None on timeout.
        if t is None:
            return float(-timeout)
        if t is False:
            return 0.0
        delay.append(t)

    return sum(delay) / len(delay)
