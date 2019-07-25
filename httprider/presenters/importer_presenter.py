from pathlib import Path

from httprider.core.api_call_interactor import api_call_interactor
from ..core.core_settings import app_settings
from ..ui.import_text_dialog import ImportTextDialog


class ImporterPresenter:
    def __init__(self, parent_view):
        self.parent = parent_view
        self.importer = None
        self.import_text_dialog = ImportTextDialog(self.parent)
        self.import_text_dialog.accepted_signal.connect(self.on_selected_text_to_import)

    def on_selected_text_to_import(self, api_calls):
        # Migration
        api_call_interactor.add_multiple_api_calls(api_calls)

    def import_collection(self, importer):
        self.importer = importer
        if self.importer.input_type == "file":
            file_location, _ = self.parent.open_file("Select File", Path("~").expanduser().as_posix())
            if file_location:
                project_info, api_calls = self.importer.import_data(file_location)
                # Migration
                api_call_interactor.add_multiple_api_calls(api_calls)

                app_settings.app_data_writer.update_project_info(project_info)

        if self.importer.input_type == "text":
            self.import_text_dialog.show_dialog(self.importer.import_data)
