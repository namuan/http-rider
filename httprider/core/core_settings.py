import logging
import logging.handlers
from pathlib import Path
from typing import Any, Union, Dict

import dataset
from PyQt5.QtCore import QSettings, QStandardPaths
from PyQt5.QtWidgets import qApp
from tinydb import TinyDB

import httprider.exporters as exporters
import httprider.importers as importers
from httprider.model.storage import Storage
from ..core import str_to_bool, import_modules, random_project_name
from ..model.app_data_cache import AppDataCache
from ..model.app_data_reader import AppDataReader
from ..model.app_data_writer import AppDataWriter
from ..model.user_data import UserProject, SavedState


class CoreSettings:

    def __init__(self):
        self.settings: QSettings = None
        self.app_name: str = None
        self.app_dir: Union[Path, Any] = None
        self.app_data_reader: AppDataReader = None
        self.app_data_writer: AppDataWriter = None
        self.app_data_cache: AppDataCache = None
        self.importers: Dict = {}
        self.exporters: Dict = {}
        self.docs_location: Path = Path(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation))

    def init(self):
        self.app_name = qApp.applicationName().lower()
        self.app_dir = Path(QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation))
        self.app_dir.mkdir(exist_ok=True)
        settings_file = f"{self.app_name}.ini"
        self.settings = QSettings(self.app_dir.joinpath(settings_file).as_posix(), QSettings.IniFormat)
        self.settings.sync()

    def init_logger(self):
        log_file = f"{self.app_name}.log"
        handlers = [
            logging.handlers.RotatingFileHandler(
                self.app_dir.joinpath(log_file),
                maxBytes=1000000, backupCount=1
            ),
            logging.StreamHandler()
        ]

        logging.basicConfig(
            handlers=handlers,
            format='%(asctime)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.DEBUG
        )
        logging.captureWarnings(capture=True)

    def init_app_data(self):
        storage = self._db_from_current_user_project()
        self.app_data_reader = AppDataReader(storage.db)
        self.app_data_writer = AppDataWriter(storage.db)
        self.app_data_cache = AppDataCache(self.app_data_reader, self.app_data_writer)

    def new_app_data(self):
        """Used when a new project is created/opened and we just wanted to switch underlying
        db_table from AppDataReader and AppDataWriter without creating a new instance"""
        storage = self._db_from_current_user_project()
        self.app_data_reader.ldb = storage.db
        self.app_data_writer.ldb = storage.db

    def init_importers(self):
        self.importers = import_modules(importers)

    def init_exporters(self):
        self.exporters = import_modules(exporters)

    def save_window_state(self, geometry, window_state):
        self.settings.setValue('geometry', geometry)
        self.settings.setValue('windowState', window_state)
        self.settings.sync()

    def save_configuration(self, updates_check):
        self.settings.setValue('startupCheck', updates_check)
        self.settings.sync()

    def load_updates_configuration(self):
        return str_to_bool(self.settings.value("startupCheck", True))

    def geometry(self):
        return self.settings.value("geometry", None)

    def window_state(self):
        return self.settings.value("windowState", None)

    def save_current_project(self, user_project: UserProject):
        self.settings.setValue('currentProjectLocation', user_project.location)
        self.settings.setValue('currentProjectState', user_project.state)
        self.settings.sync()

    def load_current_project(self):
        current_project_location = self.settings.value('currentProjectLocation', None)

        if not current_project_location:
            return self.create_new_project()

        return UserProject(
            location=current_project_location,
            state=self.settings.value('currentProjectState')
        )

    def create_new_project(self):
        user_project = UserProject(
            location=self.docs_location.joinpath(random_project_name()).as_posix(),
            state=SavedState.UN_SAVED
        )
        self.save_current_project(user_project)
        return user_project

    def _db_from_current_user_project(self):
        user_project: UserProject = self.load_current_project()
        data_location = user_project.location
        return Storage(data_location)


app_settings = CoreSettings()
