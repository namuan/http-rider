from enum import Enum
from typing import Optional

import attr


class SavedState(Enum):
    SAVED = "saved"
    UN_SAVED = "unsaved"


@attr.s(auto_attribs=True)
class UserProject(object):
    location: Optional[str]
    state: Optional[SavedState] = SavedState.UN_SAVED
