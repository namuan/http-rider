from enum import Enum, auto
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem

from httprider.exporters import exporter_plugins
from httprider.core.pygment_styles import pyg_styles
from httprider.core.constants import EXPORTER_COMBO_ROLE
from httprider.core.core_settings import app_settings
from httprider.model.app_data import ApiCall


class DisplayMode(Enum):
    SINGLE_API = auto()
    MULTIPLE_APIS = auto()


class CodeGeneratorPresenter:
    def __init__(self, view, parent=None):
        self.view = view
        self.main_window = parent
        self.mode = DisplayMode.SINGLE_API
        self.selected_api: ApiCall = None
        self.view.txt_generated_code.document().setDefaultStyleSheet(pyg_styles())

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
            item.setData(ev.exporter.name, Qt.ItemDataRole.DisplayRole)
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
            api_calls = app_settings.app_data_cache.get_all_active_api_calls()
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
