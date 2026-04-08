# flake8: noqa: E402

from pathlib import Path
import sys
from urllib.parse import urljoin

from hatchling.metadata.plugin.interface import MetadataHookInterface

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "xpip-upload"))

from xpip_build.attribute import __author__
from xpip_build.attribute import __author_email__
from xpip_build.attribute import __description__
from xpip_build.attribute import __project__
from xpip_build.attribute import __urlhome__
from xpip_build.attribute import __version__
from xpip_upload.attribute import __version__ as upload_version  # noqa:E402


def all_requirements():
    def read_requirements(path: str):
        with open(path, "r", encoding="utf-8") as rhdl:
            return rhdl.read().splitlines()

    requirements = read_requirements("requirements.txt")
    requirements.append(f"xpip-upload>={upload_version}")
    return requirements


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
