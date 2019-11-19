from enum import Enum, auto

from ..core.core_settings import app_settings
from ..model.app_data import ApiCall


class DisplayMode(Enum):
    SINGLE_API = auto()
    MULTIPLE_APIS = auto()


class FuzzTestPresenter:
    def __init__(self, view, parent=None):
        self.view = view
        self.main_window = parent
        self.mode = DisplayMode.SINGLE_API
        self.selected_api: ApiCall = None

        app_settings.app_data_reader.signals.api_call_change_selection.connect(
            self.on_updated_selected_api
        )

    def show_dialog(self):
        self.view.show()

    def on_updated_selected_api(self, api_call):
        self.selected_api = api_call
