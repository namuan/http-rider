from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import *

from ..importers import importer_plugins
from ..widgets.search_line_edit_widget import SearchLineEdit


def tool_bar_items(self):
    """Create a tool bar for the main window."""
    self.tool_bar.setObjectName("maintoolbar")
    self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tool_bar)
    self.tool_bar.setMovable(False)

    tool_bar_project_info_action = QAction(QIcon("images:info-48.png"), "Project Info", self)
    tool_bar_project_info_action.triggered.connect(self.project_info_dialog.show_dialog)
    self.tool_bar.addAction(tool_bar_project_info_action)

    self.tool_bar.addSeparator()

    tool_bar_add_call_action = QAction(QIcon("images:plus-48.png"), "Add Request", self)
    tool_bar_add_call_action.triggered.connect(self.empty_frame_presenter.on_btn_add_request)
    self.tool_bar.addAction(tool_bar_add_call_action)

    # Disabling support for adding separators
    # tool_bar_add_separator_action = QAction(QIcon("images:separator-48.png"), 'Add Separator', self)
    # tool_bar_add_separator_action.triggered.connect(self.empty_frame_presenter.on_btn_add_separator)
    # self.tool_bar.addAction(tool_bar_add_separator_action)

    tool_bar_remove_call_action = QAction(QIcon("images:minus-48.png"), "Remove Request", self)
    tool_bar_remove_call_action.triggered.connect(self.api_list_presenter.on_remove_selected_item)
    self.tool_bar.addAction(tool_bar_remove_call_action)

    self.tool_bar.addSeparator()

    # Menu for Importers
    importers = QMenu()
    for val in importer_plugins:
        imported_module = val.importer
        i_action = QAction(imported_module.name, self)
        i_action.triggered.connect(partial(self.importer_presenter.import_collection, imported_module))
        importers.addAction(i_action)

    tool_bar_import_action = QAction(QIcon("images:import-48.png"), "Import", self)
    tool_bar_import_action.setMenu(importers)

    self.tool_bar.addAction(tool_bar_import_action)

    tool_bar_export_action = QAction(QIcon("images:export-48.png"), "Export", self)
    tool_bar_export_action.triggered.connect(self.code_generator_dialog.export_single_dialog)
    self.tool_bar.addAction(tool_bar_export_action)

    tool_bar_export_all_action = QAction(QIcon("images:export-all-48.png"), "Export All", self)
    tool_bar_export_all_action.triggered.connect(self.code_generator_dialog.export_all_dialog)
    self.tool_bar.addAction(tool_bar_export_all_action)

    self.tool_bar.addSeparator()

    tool_bar_environments_action = QAction(QIcon("images:environment-48.png"), "Environments", self)
    tool_bar_environments_action.triggered.connect(self.environment_configuration_dialog.show_dialog)
    self.tool_bar.addAction(tool_bar_environments_action)

    tool_bar_envs_list = QComboBox(self)
    tool_bar_envs_list.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
    tool_bar_envs_list.setDuplicatesEnabled(False)
    tool_bar_envs_list.currentTextChanged.connect(self.envs_list_presenter.on_env_changed)
    tool_bar_envs_list_action = QWidgetAction(self)
    tool_bar_envs_list_action.setText("Environmnents")
    tool_bar_envs_list_action.setDefaultWidget(tool_bar_envs_list)
    self.tool_bar.addAction(tool_bar_envs_list_action)

    spacer = QWidget(self)
    spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    self.tool_bar.addWidget(spacer)

    tool_bar_multi_share_call_action = QAction(QIcon("images:share-all-48.png"), "Share All", self)
    tool_bar_multi_share_call_action.triggered.connect(self.share_preview_dialog.show_multiple_exchanges_preview)
    self.tool_bar.addAction(tool_bar_multi_share_call_action)

    tool_bar_multi_run_call_action = QAction(QIcon("images:multirun-48.png"), "Run All", self)
    tool_bar_multi_run_call_action.triggered.connect(self.on_run_all_api_calls)
    self.tool_bar.addAction(tool_bar_multi_run_call_action)

    tool_bar_search_field = SearchLineEdit(self)
    tool_bar_search_field.textChanged.connect(self.api_list_presenter.on_search_query)
    tool_bar_search_field_action = QWidgetAction(self)
    tool_bar_search_field_action.setDefaultWidget(tool_bar_search_field)
    self.tool_bar.addAction(tool_bar_search_field_action)

    tool_bar_tags_list = QComboBox(self)
    tool_bar_tags_list.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
    tool_bar_tags_list.setDuplicatesEnabled(False)
    tool_bar_tags_list.currentTextChanged.connect(self.tags_list_presenter.on_tag_changed)
    tool_bar_tags_list_action = QWidgetAction(self)
    tool_bar_tags_list_action.setText("Tags")
    tool_bar_tags_list_action.setDefaultWidget(tool_bar_tags_list)
    self.tool_bar.addAction(tool_bar_tags_list_action)

    tool_bar_configure_action = QAction(QIcon("images:configure-48.png"), "Settings", self)
    tool_bar_configure_action.triggered.connect(self.configuration_dialog.show_dialog)
    self.tool_bar.addAction(tool_bar_configure_action)

    tool_bar_update_available = QAction(QIcon("images:download-disabled-48.png"), "Update Available", self)
    tool_bar_update_available.setEnabled(False)
    tool_bar_update_available.triggered.connect(self.open_releases_page)

    self.tool_bar.addAction(tool_bar_update_available)
