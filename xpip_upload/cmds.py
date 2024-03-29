# coding=utf-8

from argparse import ArgumentParser
from argparse import Namespace
from configparser import ConfigParser
import os
import sys
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

from twine.commands.check import main as check
from twine.commands.upload import main as upload
from twine.package import MetadataValue
from twine.package import PackageFile
from twine.utils import DEFAULT_CONFIG_FILE
from twine.utils import DEFAULT_REPOSITORY as DEFAULT_REPO_URL

from .util import __description__
from .util import __url_home__

try:
    from argcomplete import autocomplete
except ModuleNotFoundError:
    pass


def get_project_name(filepath: str) -> str:
    pkgf: PackageFile = PackageFile.from_filename(filepath, comment=None)
    project_name: MetadataValue = pkgf.metadata_dictionary()["name"]
    assert isinstance(project_name, str)
    return project_name


_ClassInfo = Union[type, Tuple["_ClassInfo", ...]]


class parser:
    DEFAULT_REPO = "pypi"
    OPT_REPO = "repository"
    OPT_USERNAME = "username"
    OPT_PASSWORD = "password"
    OPT_TOKEN = "token"
    TOKEN_USERNAME = "__token__"

    def __init__(self, args: Namespace):
        self.__args: Namespace = args
        config_file: str = self.__safe_getattr("config_file", List)[0]
        assert isinstance(config_file, str)
        self.__path = os.path.expanduser(config_file)
        self.__conf = ConfigParser()
        if os.path.isfile(self.__path):
            self.__conf.read(self.__path)

    @property
    def args(self) -> Namespace:
        return self.__args

    @property
    def conf(self) -> ConfigParser:
        return self.__conf

    @property
    def verbose(self) -> bool:
        return self.__safe_getattr("verbose", bool)

    @property
    def allow_repositorys(self) -> List[str]:
        sections: List[str] = [self.DEFAULT_REPO]
        for section in self.conf.sections():
            if section not in ["distutils"] and section not in sections:
                sections.append(section)
        return sections

    def __safe_getattr(self, name: str, types: Optional[_ClassInfo] = None):
        value = getattr(self.args, name)
        if types is not None:
            assert isinstance(value, types)
        return value

    def __get_reponame(self, package: str) -> str:
        repository = self.__safe_getattr("repository", List)[0]
        if isinstance(repository, str) and repository != "":
            return repository
        name = get_project_name(package)
        return name if name in self.allow_repositorys else self.DEFAULT_REPO

    def __get_repourl(self, repo: str) -> str:
        repository_url = self.__safe_getattr("repository_url", List)[0]
        if isinstance(repository_url, str):
            return repository_url  # override --repository
        if self.conf.has_option(repo, self.OPT_REPO):
            return self.conf[repo][self.OPT_REPO]
        return DEFAULT_REPO_URL

    def __get_username(self, repo: str) -> Optional[str]:
        token: Optional[str] = self.__safe_getattr("token", List)[0]
        if isinstance(token, str):
            return self.TOKEN_USERNAME  # override --username
        if self.conf.has_option(repo, self.OPT_TOKEN):
            return self.TOKEN_USERNAME  # override username config
        if self.conf.has_option(repo, self.OPT_USERNAME):
            return self.conf[repo][self.OPT_USERNAME]
        return None

    def __get_password(self, repo: str) -> Optional[str]:
        token: Optional[str] = self.__safe_getattr("token", List)[0]
        if isinstance(token, str):
            return token  # override --password
        if self.conf.has_option(repo, self.OPT_TOKEN):
            return self.conf[repo][self.OPT_TOKEN]  # override password config
        if self.conf.has_option(repo, self.OPT_PASSWORD):
            return self.conf[repo][self.OPT_PASSWORD]
        return None

    def get_upload_args(self, package: str) -> List[str]:
        reponame: str = self.__get_reponame(package)
        repourl: str = self.__get_repourl(reponame)
        username: Optional[str] = self.__get_username(reponame)
        password: Optional[str] = self.__get_password(reponame)

        upload_args: List[str] = [f"--repository-url={repourl}"]
        if isinstance(username, str):
            upload_args.append(f"--username={username}")
        if isinstance(password, str):
            upload_args.append(f"--password={password}")
        if self.verbose:
            upload_args.append("--verbose")
        upload_args.append(package)
        return upload_args


def add_cmd(_arg: ArgumentParser, argv: Optional[List[str]] = None):
    _arg.add_argument("-d", "--debug", action="store_true",
                      help="show debug information")
    marg = _arg.add_mutually_exclusive_group()
    marg.add_argument("--no-check", action="store_true",
                      help="not check package files")
    marg.add_argument("--only-check", action="store_true",
                      help="only check package files")
    _arg.add_argument("--verbose", action="store_true",
                      help="show twine verbose output")
    config_default = f"twine default use {DEFAULT_CONFIG_FILE}"
    config_help = f"config file to use, {config_default}"
    _arg.add_argument("--config-file", type=str, nargs=1, metavar="CONFIG",
                      default=[DEFAULT_CONFIG_FILE], help=config_help)
    _arg.add_argument("--token", type=str, nargs=1, metavar="TOKEN",
                      default=[os.environ.get("TOKEN", None)],
                      help="The token to authenticate to the repository "
                      "(package index) as, can also be set via TOKEN"
                      "environment variable, "
                      "this overrides username and password")
    args, _ = _arg.parse_known_args(argv)
    _arg.add_argument("--repository", type=str, nargs=1, default=[None],
                      choices=parser(args).allow_repositorys,
                      help="The repository (package index) to upload the "
                      "package to, should be a section in the config file, "
                      "this overrides project name or pypi")
    _arg.add_argument("--repository-url", type=str,
                      nargs=1, metavar="URL", default=[None],
                      help="The repository (package index) URL to upload the "
                      "package to, this overrides --repository")
    _arg.add_argument("dists", metavar="PACKAGE", nargs="+",
                      help="all distribution files to upload")


def run_cmd(args: Namespace) -> int:
    dists: Set[str] = set()
    for i in args.dists:
        if not isinstance(i, str):
            continue
        if not os.path.isfile(i):
            continue
        segments = i.split(".")  # filetype: ".whl" and ".tar.gz"
        if segments[-1] == "whl" or segments[-2:] == ["tar", "gz"]:
            dists.add(i)

    _parser = parser(args)
    for pkg in dists:
        if not args.no_check:
            check_args: List[str] = ["--strict", pkg]
            check(check_args)
        if not args.only_check:
            upload(_parser.get_upload_args(pkg))
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    _arg = ArgumentParser(prog="xpip-upload", description=__description__,
                          epilog=f"For more, please visit {__url_home__}")
    add_cmd(_arg, argv)

    try:
        autocomplete(_arg)
    except NameError:
        pass

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
