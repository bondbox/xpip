# flake8: noqa: E402

from pathlib import Path
import sys
from urllib.parse import urljoin

from hatchling.metadata.plugin.interface import MetadataHookInterface

sys.path.insert(0, str(Path(__file__).parent))

from xpip_upload.attribute import __author__
from xpip_upload.attribute import __author_email__
from xpip_upload.attribute import __description__
from xpip_upload.attribute import __project__
from xpip_upload.attribute import __urlhome__
from xpip_upload.attribute import __version__


class CustomMetadataHook(MetadataHookInterface):
    def update(self, metadata):
        metadata["name"] = __project__
        metadata["version"] = __version__
        metadata["description"] = __description__
        metadata["authors"] = [
            {"name": __author__, "email": __author_email__},
        ]
        metadata["urls"] = {
            "Homepage": __urlhome__,
            "Source Code": __urlhome__,
            "Bug Tracker": urljoin(__urlhome__, "issues"),
            "Documentation": __urlhome__,
        }
