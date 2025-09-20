__version__ = "0.6.4"
__appname__ = "httprider"
__description__ = "Simple and Powerful cross-platform Rest API client"
__desktopid__ = "dev.deskriders.HttpRider"

from pathlib import Path

from PyQt6.QtCore import QDir

from httprider.core import *
from httprider.core.constants import *
from httprider.core.core_settings import app_settings as app_settings
from httprider.core.generators import *
from httprider.core.json_data_generator import *
from httprider.core.pygment_styles import *
from httprider.model import *
from httprider.presenters import *

resources_path = Path(__file__).parent.parent / "resources"
QDir.addSearchPath("themes", resources_path.joinpath("themes").as_posix())
QDir.addSearchPath("images", resources_path.joinpath("images").as_posix())
QDir.addSearchPath("fonts", resources_path.joinpath("fonts").as_posix())
QDir.addSearchPath("icons", resources_path.joinpath("icons").as_posix())
