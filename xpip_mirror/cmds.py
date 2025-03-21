# coding=utf-8

import concurrent.futures
import socket
import sys
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Sequence
from typing import Tuple
from urllib.parse import urlparse

from pip._internal.cli.main import main as pipcli
from tabulate import tabulate
from xkits import add_command
from xkits import argp
from xkits import commands
from xkits import run_command

from xpip_mirror.attribute import __description__
from xpip_mirror.attribute import __urlhome__
from xpip_mirror.attribute import __version__
from xpip_mirror.util import DIR_CONF
from xpip_mirror.util import ping_second
from xpip_mirror.util import toml_dump
from xpip_mirror.util import toml_load

CONF_MIRRORS = f"{DIR_CONF}/mirrors.toml"
CONF_MIRRORS_NAME: List[str] = []


class MIRROR(NamedTuple):
    name: str
    url: str
    hostname: str
    address: str
    ping_ms: float


def get_mirror(name: str, url: str) -> MIRROR:
    if (hostname := urlparse(url).hostname) is None:
        return MIRROR(name, url, "ERROR", "UNKOWN", 0.0)

    try:
        address = socket.gethostbyname(hostname)
        ping_ms = ping_second(address, 10, 1) * 1000
    except socket.error:
        address = "UNKOWN"
        ping_ms = 0.0
    return MIRROR(name, url, hostname, address, ping_ms)


def get_mirrors(mirrors: Dict[str, Dict[str, str]]) -> List[MIRROR]:
    _mirrors: List[MIRROR] = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for key in mirrors:
            mirror = mirrors[key]
            url = mirror["url"]
            futures.append(executor.submit(get_mirror, key, url))
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if isinstance(result, MIRROR):
                _mirrors.append(result)
    # sort by speed
    _mirrors.sort(key=lambda x: x.ping_ms, reverse=False)
    # move "timeout" values to the end of the list
    _mirrors = sorted(_mirrors, key=lambda x: x.ping_ms <= 0)
    return _mirrors


def choice_mirror(mirrors: List[MIRROR],
                  name: Optional[str] = None) -> Optional[MIRROR]:
    if name is not None:
        find = False
        for m in mirrors:
            if m.name == name:
                find = True
                if m.hostname == "ERROR":
                    sys.stderr.write(f"URL error: {m.url}\n")
                    break
                if m.address == "UNKOWN":
                    sys.stderr.write(f"cannot get ip address: {m.hostname}\n")
                    break
                if m.ping_ms < 0:
                    sys.stderr.write(f"ping timeout: {m.address}\n")
                    break
                return m
        if not find:
            sys.stderr.write(f"cannot find mirror: {name}\n")
        sys.stdout.flush()
    elif len(mirrors) > 0 and mirrors[0].ping_ms > 0:
        # choice the best of mirror
        return mirrors[0]

    return None


@add_command("list", help="list all mirrors")
def add_cmd_list(_arg: argp):
    pass


@run_command(add_cmd_list)
def run_cmd_list(cmds: commands) -> int:
    mirrors: List[MIRROR] = get_mirrors(cmds.args.mirrors)
    # print table format
    tabular_data: List[Tuple[str, str, str, str]] = []
    for m in mirrors:
        _host = f"{m.hostname} ({m.address})"
        _ping = f"{m.ping_ms:.01f}" if m.ping_ms > 0 else "timeout"
        tabular_data.append((m.name, m.url, _host, _ping))
    table = tabulate(tabular_data,
                     headers=["name", "URL", "HOST", "PING(ms)"],
                     floatfmt=".1f")  # tablefmt="simple"
    sys.stderr.write(f"{table}\n")
    sys.stdout.flush()
    # choice the best of mirror
    best = choice_mirror(mirrors)
    if best is not None:
        sys.stderr.write("\nSuggest using the installation command:\n"
                         f"pip install -i {best.url} <package-name>\n")
        sys.stdout.flush()
    return 0


@add_command("get", help="get mirror's URL")
def add_cmd_get(_arg: argp):
    global CONF_MIRRORS_NAME  # pylint: disable=global-variable-not-assigned
    _arg.add_argument("name", metavar="NAME", type=str, nargs="?",
                      choices=CONF_MIRRORS_NAME, help="specify name")


@run_command(add_cmd_get)
def run_cmd_get(cmds: commands) -> int:
    _name = cmds.args.name
    if _name is not None and _name in cmds.args.mirrors:
        mirror: dict = cmds.args.mirrors[_name]
        sys.stderr.write(f"{mirror['url']}\n")
        sys.stdout.flush()
    return 0


@add_command("set", help="set mirror's URL")
def add_cmd_set(_arg: argp):
    global CONF_MIRRORS_NAME  # pylint: disable=global-variable-not-assigned
    _arg.add_argument("name", metavar="NAME", type=str, nargs="?",
                      choices=CONF_MIRRORS_NAME, help="specify name")
    _arg.add_argument("url", metavar="URL", type=str,
                      nargs="?", help="specify URL")


@run_command(add_cmd_set)
def run_cmd_set(cmds: commands) -> int:
    _name = cmds.args.name
    _url = cmds.args.url
    if _name is not None and _url is not None:
        mirror = {_name: {"url": _url}}
        cmds.args.mirrors.update(mirror)
        toml_dump(cmds.args.config, cmds.args.mirrors)
    return 0


@add_command("now", help="show config mirror")
def add_cmd_now(_arg: argp):
    pass


@run_command(add_cmd_now)
def run_cmd_now(cmds: commands) -> int:  # pylint: disable=unused-argument
    pipcli("config get global.index-url".split())
    return 0


@add_command("choice", help="choice mirror")
def add_cmd_choice(_arg: argp):
    global CONF_MIRRORS_NAME  # pylint: disable=global-variable-not-assigned
    _arg.add_argument("name", nargs="?", type=str,
                      metavar="NAME", choices=CONF_MIRRORS_NAME,
                      help="specify name, default choice the best")


@run_command(add_cmd_choice)
def run_cmd_choice(cmds: commands) -> int:
    result: int = 0
    mirrors = get_mirrors(cmds.args.mirrors)
    best = choice_mirror(mirrors, cmds.args.name)
    if best is not None:
        result = pipcli(f"config set global.index-url {best.url}".split())
        if result == 0:
            sys.stderr.write(f"choice {best.name}: {best.url}\n")
            sys.stdout.flush()
    return result


@add_command("mirror")
def add_cmd(_arg: argp):
    _arg.add_argument("-c", "--config", nargs="?", type=str,
                      const=CONF_MIRRORS, default=CONF_MIRRORS,
                      help="specify config file")
    global CONF_MIRRORS_NAME  # pylint: disable=global-statement
    args = _arg.preparse_from_sys_argv()
    CONF_MIRRORS_NAME = list(toml_load(args.config).keys())


@run_command(add_cmd, add_cmd_list, add_cmd_get, add_cmd_set,
             add_cmd_now, add_cmd_choice)
def run_cmd(cmds: commands) -> int:
    cmds.args.mirrors = toml_load(cmds.args.config)
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cmds = commands()
    cmds.version = __version__
    return cmds.run(
        root=add_cmd,
        argv=argv,
        description=__description__,
        epilog=f"For more, please visit {__urlhome__}.")
