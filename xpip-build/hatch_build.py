# flake8: noqa: E402

from pathlib import Path
import sys
from typing import List
from urllib.parse import urljoin

from hatchling.metadata.plugin.interface import MetadataHookInterface
from packaging.requirements import Requirement

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "xpip-upload"))

from xpip_build.attribute import __author__
from xpip_build.attribute import __author_email__
from xpip_build.attribute import __description__
from xpip_build.attribute import __project__
from xpip_build.attribute import __urlhome__
from xpip_build.attribute import __version__
from xpip_upload.attribute import __version__ as upload_version  # noqa:E402


def all_requirements() -> List[str]:
    def read_requirements(path: str = "requirements.txt") -> List[Requirement]:
        with open(path, "r", encoding="utf-8") as rhdl:
            return [Requirement(line) for line in rhdl.read().splitlines()]

    (requirements := read_requirements()).append(Requirement(f"xpip-upload>={upload_version}"))  # noqa:E501
    return [str(dependence) for dependence in requirements]


class CustomMetadataHook(MetadataHookInterface):
    def update(self, metadata):
        metadata["name"] = __project__
        metadata["version"] = __version__
        metadata["description"] = __description__
        metadata["dependencies"] = all_requirements()
        metadata["authors"] = [
            {"name": __author__, "email": __author_email__},
        ]
        metadata["urls"] = {
            "Homepage": __urlhome__,
            "Source Code": __urlhome__,
            "Bug Tracker": urljoin(__urlhome__, "issues"),
            "Documentation": __urlhome__,
        }
