import logging
from functools import partial
from typing import TYPE_CHECKING

from PyQt6.QtGui import QAction

from httprider.importers import importer_plugins

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QMenu


# ruff: noqa: PLR0915
def menu_items(self):
    # File Menu
    new_action = QAction("&New", self)
    new_action.setShortcut("Ctrl+N")
    new_action.triggered.connect(self.file_menu_presenter.on_file_new)

    open_action = QAction("&Open ...", self)
    open_action.setShortcut("Ctrl+O")
    open_action.triggered.connect(self.file_menu_presenter.on_file_open)

    save_action = QAction("&Save", self)
    save_action.setShortcut("Ctrl+S")
    save_action.triggered.connect(self.file_menu_presenter.on_file_save)

    save_as_action = QAction("Save &As...", self)
    save_as_action.triggered.connect(self.file_menu_presenter.on_file_save_as)

    f: QMenu = self.menu_bar.addMenu("&File")
    f.addAction(new_action)
    f.addAction(open_action)
    f.addSeparator()
    f.addAction(save_action)
    f.addAction(save_as_action)

    # Separate Import menu with dynamic plugin discovery
    import_menu: QMenu = self.menu_bar.addMenu("&Import")
    for plugin in importer_plugins:
        imported_module = plugin.importer
        import_action = QAction(imported_module.name, self)
        import_action.triggered.connect(partial(self.importer_presenter.import_collection, imported_module))
        import_menu.addAction(import_action)
        logging.debug(f"Added import plugin: {imported_module.name}")

    single_request = QAction("&Send", self)
    single_request.setShortcut("Ctrl+Return")
    single_request.triggered.connect(self.request_presenter.on_btn_send_request)

    multiple_request = QAction("&Send All", self)
    multiple_request.setShortcut("Ctrl+Shift+Return")
    multiple_request.triggered.connect(self.api_list_presenter.run_all_api_calls)

    single_export = QAction("&Export", self)
    single_export.setShortcut("Ctrl+E")
    single_export.triggered.connect(self.code_generator_dialog.export_single_dialog)

    multiple_export = QAction("&Export All", self)
    multiple_export.setShortcut("Ctrl+Shift+E")
    multiple_export.triggered.connect(self.code_generator_dialog.export_all_dialog)

    generate_data = QAction("&Insert Variables", self)
    generate_data.setShortcut("Ctrl+I")
    generate_data.triggered.connect(self.request_presenter.on_show_data_generator_dialog)

    r: QMenu = self.menu_bar.addMenu("&Requests")
    r.addAction(single_request)
    r.addAction(multiple_request)
    r.addSeparator()
    r.addAction(single_export)
    r.addAction(multiple_export)
    r.addSeparator()
    r.addAction(generate_data)

    # Environments Menu
    export_env_action = QAction("&Export", self)
    export_env_action.triggered.connect(self.env_menu_presenter.on_export)

    import_env_action = QAction("&Import", self)
    import_env_action.triggered.connect(self.env_menu_presenter.on_import)

    r: QMenu = self.menu_bar.addMenu("&Environments")
    r.addAction(export_env_action)
    r.addAction(import_env_action)
