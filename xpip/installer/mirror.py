# coding=utf-8

from argparse import ArgumentParser
import concurrent.futures
from errno import ENOENT
import socket
import sys
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple
from urllib.parse import urlparse

from argcomplete import autocomplete
from pip._internal.cli.main import main as pipcli
from tabulate import tabulate

from ..utils import DIR_CONF
from ..utils import URL_PROG
from ..utils import ping_second
from ..utils import toml_dump
from ..utils import toml_load

CONF_MIRRORS = f"{DIR_CONF}/mirrors.toml"
EPILOG = f"For more, please visit {URL_PROG}"


class MIRROR(NamedTuple):
    name: str
    url: str
    hostname: str
    address: str
    ping_ms: float


def get_mirror(name: str, url: str) -> MIRROR:
    try:
        hostname = urlparse(url).hostname
    except TypeError:
        hostname = None

    if hostname is None:
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


def add_cmd_list(_arg: ArgumentParser):
    pass


def run_cmd_list(args) -> int:
    mirrors: List[MIRROR] = get_mirrors(args.mirrors)
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


def add_cmd_get(_arg: ArgumentParser):
    _arg.add_argument("name", metavar="NAME", type=str,
                      nargs="?", help="specify name")


def run_cmd_get(args) -> int:
    _name = args.name
    if _name is not None and _name in args.mirrors:
        mirror: dict = args.mirrors[_name]
        sys.stderr.write(f"{mirror['url']}\n")
        sys.stdout.flush()
    return 0


def add_cmd_set(_arg: ArgumentParser):
    _arg.add_argument("name", metavar="NAME", type=str,
                      nargs="?", help="specify name")
    _arg.add_argument("url", metavar="URL", type=str,
                      nargs="?", help="specify URL")


def run_cmd_set(args) -> int:
    _name = args.name
    _url = args.url
    if _name is not None and _url is not None:
        mirror = {_name: {"url": _url}}
        args.mirrors.update(mirror)
        toml_dump(args.config, args.mirrors)
    return 0


def add_cmd_now(_arg: ArgumentParser):
    pass


def run_cmd_now(args) -> int:
    pipcli("config get global.index-url".split())
    return 0


def add_cmd_choice(_arg: ArgumentParser):
    _arg.add_argument("name", nargs="?", type=str, metavar="NAME",
                      help="specify name, default choice the best")


def run_cmd_choice(args) -> int:
    mirrors = get_mirrors(args.mirrors)
    best = choice_mirror(mirrors, args.name)
    if best is not None:
        result = pipcli(f"config set global.index-url {best.url}".split())
        if result == 0:
            sys.stderr.write(f"choice {best.name}: {best.url}\n")
            sys.stdout.flush()
        return result
    return 0


def add_cmd(_arg: ArgumentParser):
    _arg.add_argument("-d", "--debug", action="store_true",
                      help="show debug information")
    _arg.add_argument("-c", "--config", nargs="?", type=str,
                      const=CONF_MIRRORS, default=CONF_MIRRORS,
                      help="specify config file")
    _sub = _arg.add_subparsers(dest="sub_mirror")
    add_cmd_list(_sub.add_parser("list", help="list all mirrors",
                                 description="list all mirrors",
                                 epilog=EPILOG))
    add_cmd_get(_sub.add_parser("get", help="get mirror's URL",
                                description="get mirror's URL",
                                epilog=EPILOG))
    add_cmd_set(_sub.add_parser("set", help="set mirror's URL",
                                description="set mirror's URL",
                                epilog=EPILOG))
    add_cmd_now(_sub.add_parser("now", help="show config mirror",
                                description="show config mirror",
                                epilog=EPILOG))
    add_cmd_choice(_sub.add_parser("choice", help="choice mirror",
                                   description="choice mirror",
                                   epilog=EPILOG))


def run_cmd(args) -> int:
    cmds = {
        "list": run_cmd_list,
        "get": run_cmd_get,
        "set": run_cmd_set,
        "now": run_cmd_now,
        "choice": run_cmd_choice,
    }
    if not hasattr(args, "sub_mirror") or args.sub_mirror not in cmds:
        return ENOENT
    args.mirrors = toml_load(args.config)
    return cmds[args.sub_mirror](args)


def main(argv: Optional[List[str]] = None) -> int:
    _arg = ArgumentParser(prog="xpip-mirror",
                          description="pip mirror management",
                          epilog=EPILOG)
    add_cmd(_arg)
    autocomplete(_arg)
    args = _arg.parse_args(argv)

    if hasattr(args, "debug") and args.debug:
        sys.stdout.write(f"{args}\n")
        sys.stdout.flush()

    try:
        return run_cmd(args)
    except KeyboardInterrupt:
        return 0
    except BaseException as e:
        if hasattr(args, "debug") and args.debug:
            raise e
        sys.stderr.write(f"{e}\n")
        sys.stderr.flush()
        return 10000
