from enum import Enum, auto
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem

from ..exporters import exporter_plugins
from ..core import styles_from_file
from ..core.constants import EXPORTER_COMBO_ROLE
from ..core.core_settings import app_settings
from ..model.app_data import ApiCall


class DisplayMode(Enum):
    SINGLE_API = auto()
    MULTIPLE_APIS = auto()


class CodeGeneratorPresenter:
    def __init__(self, view, parent=None):
        self.view = view
        self.main_window = parent
        self.mode = DisplayMode.SINGLE_API
        self.selected_api: ApiCall = None
        self.pyg_styles = styles_from_file(":/themes/pyg.css")
        self.view.txt_generated_code.document().setDefaultStyleSheet(self.pyg_styles)

        self.view.cmb_exporters.currentIndexChanged[int].connect(
            self.on_exporter_change
        )
        self.view.btn_copy_code.pressed.connect(self.on_copy_clipboard)
        self.view.btn_export_code.pressed.connect(self.on_export_file)

        app_settings.app_data_reader.signals.api_call_change_selection.connect(
            self.on_updated_selected_api
        )

    def show_dialog(self):
        self.view.cmb_exporters.clear()

        for ek, ev in exporter_plugins.items():
            item: QStandardItem = QStandardItem()
            item.setData(ev.exporter.name, Qt.DisplayRole)
            item.setData(ek, EXPORTER_COMBO_ROLE)
            self.view.cmb_exporters.addItem(ev.exporter.name, item)

        self.view.show()

    def on_updated_selected_api(self, api_call):
        self.selected_api = api_call

    def on_exporter_change(self, _):
        item: QStandardItem = self.view.cmb_exporters.currentData()
        if not item:
            return

        self.view.txt_generated_code.clear()
        selected_name = item.data(EXPORTER_COMBO_ROLE)
        selected_exporter = exporter_plugins.get(selected_name)
        self.generate_code(selected_exporter)

    def generate_code(self, selected_exporter):
        if self.mode == DisplayMode.SINGLE_API and self.selected_api:
            generated_code = selected_exporter.exporter.export_data([self.selected_api])
        else:
            app_state = app_settings.app_data_cache.get_app_state()
            api_calls = [
                api_call
                for api_call in app_settings.app_data_cache.filter_api_calls(
                    search_query=app_state.selected_search,
                    search_tag=app_state.selected_tag,
                )
                if api_call.enabled
            ]

            generated_code = selected_exporter.exporter.export_data(api_calls)

        self.view.txt_generated_code.appendHtml(generated_code)

    def on_copy_clipboard(self):
        self.view.txt_generated_code.selectAll()
        self.view.txt_generated_code.copy()
        self.main_window.status_bar.showMessage("Copied to clipboard", 2000)

    def on_export_file(self):
        file_location, _ = self.main_window.save_file(
            "Select File", Path("~").expanduser().as_posix()
        )
        if file_location:
            file = Path(file_location)
            file.write_text(self.view.txt_generated_code.toPlainText())
            self.main_window.status_bar.showMessage(f"File saved {file_location}")
