__version__ = "0.6.4"
__appname__ = "httprider"
__description__ = "Simple and Powerful cross-platform Rest API client"
__desktopid__ = "dev.deskriders.HttpRider"

from pathlib import Path

import sqlalchemy.dialects.sqlite
import sqlalchemy.sql.default_comparator
from pygments.styles.default import DefaultStyle
from PyQt6.QtCore import QDir

resources_path = Path(__file__).parent.parent / "resources"
QDir.addSearchPath("themes", resources_path.joinpath("themes").as_posix())
QDir.addSearchPath("images", resources_path.joinpath("images").as_posix())
QDir.addSearchPath("fonts", resources_path.joinpath("fonts").as_posix())
QDir.addSearchPath("icons", resources_path.joinpath("icons").as_posix())
