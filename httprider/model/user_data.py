from enum import Enum

import attr


class SavedState(Enum):
    SAVED = "saved"
    UN_SAVED = "unsaved"


@attr.s(auto_attribs=True)
class UserProject:
    location: str | None
    state: SavedState | None = SavedState.UN_SAVED
