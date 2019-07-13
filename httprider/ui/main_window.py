import logging
import sys
import traceback

from PyQt5.QtGui import QDesktopServices, QCloseEvent, QIcon

from ..presenters import *
from ..generated.base_window import Ui_MainWindow
from ..ui.code_generator_dialog import CodeGeneratorDialog
from ..ui.configuration_dialog import ConfigurationDialog
from ..ui.environment_configuration_dialog import EnvironmentConfigurationDialog
from ..ui.menus import menu_items
from ..ui.shortcuts import shortcut_items
from ..ui.progress_dialog import ProgressDialog
from ..ui.project_info_dialog import ProjectInfoDialog
from ..ui.toolbar import tool_bar_items
from ..ui.updater_dialog import Updater


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # Add Components on Main Window
        self.setup_empty_frame()
        self.updater = Updater(self)
        self.menu_bar = self.menuBar()
        self.tool_bar = QToolBar()
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready', 5000)

        # Initialise Presenters
        self.presenter = MainPresenter(self)

        self.empty_frame_presenter = EmptyFramePresenter(self)
        self.api_list_presenter = ApiListPresenter(self)
        self.request_presenter = RequestPresenter(self)
        self.exchange_presenter = ExchangePresenter(self)
        self.importer_presenter = ImporterPresenter(self)
        self.tags_list_presenter = TagsListPresenter(self)
        self.envs_list_presenter = EnvironmentsListPresenter(self)
        self.api_calls_history_presenter = ApiCallsHistoryPresenter(self)
        self.file_menu_presenter = FileMenuPresenter(self)

        # Custom Dialogs
        self.configuration_dialog = ConfigurationDialog(self)
        self.progress_dialog = ProgressDialog(self)
        self.environment_configuration_dialog = EnvironmentConfigurationDialog(self)
        self.project_info_dialog = ProjectInfoDialog(self)
        self.code_generator_dialog = CodeGeneratorDialog(self)

        # Initialise Components
        menu_items(self)
        tool_bar_items(self)
        shortcut_items(self)

        # Initialise Sub-Systems
        sys.excepthook = MainWindow.log_uncaught_exceptions

    def setup_empty_frame(self):
        self.frame_request_response.hide()
        self.empty_frame = QFrame(self.splitter)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setHeightForWidth(self.empty_frame.sizePolicy().hasHeightForWidth())
        self.empty_frame.setSizePolicy(sizePolicy)
        self.empty_frame.setObjectName("empty_frame")
        self.btn_add_request = QPushButton(self.empty_frame)
        self.gridLayout = QGridLayout(self.empty_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_add_request.sizePolicy().hasHeightForWidth())
        self.btn_add_request.setSizePolicy(sizePolicy)
        self.gridLayout.addWidget(self.btn_add_request, 0, 1, 1, 1)
        self.btn_add_request.setText("Add Request")

    def on_run_all_api_calls(self):
        self.request_presenter.update_current_api_call()
        self.api_list_presenter.run_all_api_calls()

    @staticmethod
    def log_uncaught_exceptions(cls, exc, tb) -> None:
        logging.critical(''.join(traceback.format_tb(tb)))
        logging.critical('{0}: {1}'.format(cls, exc))

    # Main Window events
    def resizeEvent(self, event):
        self.presenter.after_window_loaded()

    def refresh_all_views(self):
        self.api_list_presenter.refresh()
        self.tags_list_presenter.refresh()
        self.envs_list_presenter.refresh()

    def closeEvent(self, event: QCloseEvent):
        logging.info("Received close event")
        event.accept()
        self.presenter.shutdown()
        try:
            qApp.exit(0)
        except:
            pass

    # End Main Window events
    def check_updates(self):
        self.updater.check()

    def update_available(self, latest, current):
        update_available = True if latest > current else False
        logging.info(f"Update Available ({latest} > {current}) ? ({update_available}) Enable Toolbar Icon")
        if update_available:
            toolbar_actions = self.tool_bar.actions()
            updates_action = next(act for act in toolbar_actions if act.text() == 'Update Available')
            if updates_action:
                updates_action.setIcon(QIcon(":/images/download-48.png"))
                updates_action.setEnabled(True)

    def open_releases_page(self) -> None:
        QDesktopServices.openUrl(self.releases_page)

    # @todo: Remove usages and use one under ui module
    def open_file(self, dialog_title, dialog_location, file_filter=None):
        return QFileDialog.getOpenFileName(
            self,
            dialog_title,
            dialog_location,
            filter=file_filter
        )

    # @todo: Remove usages and use one under ui module
    def save_file(self, dialog_title, dialog_location, file_filter=None):
        return QFileDialog.getSaveFileName(
            self,
            dialog_title,
            dialog_location,
            filter=file_filter
        )
