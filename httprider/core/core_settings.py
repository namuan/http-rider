import logging
import logging.handlers
import platform
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QSettings, QStandardPaths
from PyQt6.QtWidgets import QApplication

from httprider.core import random_project_name, str_to_bool
from httprider.model.app_configuration import AppConfiguration
from httprider.model.app_data_cache import AppDataCache
from httprider.model.app_data_reader import AppDataReader
from httprider.model.app_data_writer import AppDataWriter
from httprider.model.storage import Storage
from httprider.model.user_data import SavedState, UserProject

CURRENT_PROJECT_STATE_KEY = "currentProjectState"
CURRENT_PROJECT_LOCATION_KEY = "currentProjectLocation"
HTTPS_PROXY_KEY = "httpsProxy"
HTTP_PROXY_KEY = "httpProxy"
NO_PROXY_KEY = "noProxy"
TLS_VERIFICATION_KEY = "tlsVerification"
ALLOW_REDIRECTS_KEY = "allowRedirects"
STARTUP_CHECK_KEY = "startupCheck"
WINDOW_STATE_KEY = "windowState"
GEOMETRY_KEY = "geometry"
REQUEST_TIMEOUT_SECS = "requestTimeoutSecs"
PRINT_SHARE_SERVER = "printShareServer"


class CoreSettings:
    def __init__(self):
        self.settings: QSettings = None
        self.app_name: str = None
        self.app_dir: Path | Any = None
        self.logs_dir: Path | Any = None
        self.app_data_reader: AppDataReader = None
        self.app_data_writer: AppDataWriter = None
        self.app_data_cache: AppDataCache = None
        self.docs_location: Path = Path(
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation),
        )

    def init(self):
        self.app_name = QApplication.instance().applicationName().lower()
        self.app_dir = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation))
        self.app_dir.mkdir(exist_ok=True)

        # Set up platform-aware logs directory
        self._setup_logs_directory()

        settings_file = f"{self.app_name}.ini"
        self.settings = QSettings(self.app_dir.joinpath(settings_file).as_posix(), QSettings.Format.IniFormat)
        self.settings.sync()

    def _setup_logs_directory(self):
        """Set up platform-appropriate logging directory."""
        home_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)

        if platform.system() == "Darwin":  # macOS
            # Follow macOS convention: ~/Library/Logs/
            logs_base_dir = Path(home_path) / "Library" / "Logs"
        elif platform.system() == "Windows":
            # Use AppData for Windows
            app_data_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
            logs_base_dir = Path(app_data_path) / "logs"
        else:
            # Linux and other Unix-like systems: use ~/.local/share/app/logs
            app_data_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
            logs_base_dir = Path(app_data_path) / "logs"

        # Create application-specific logs directory
        self.logs_dir = logs_base_dir / QApplication.applicationName()
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def init_logger(self):
        log_file = "httprider.log"

        # Logs directory is already set up in init method
        handlers = [
            logging.handlers.RotatingFileHandler(
                self.logs_dir.joinpath(log_file),
                maxBytes=1_000_000,
                backupCount=5,
            ),
            logging.StreamHandler(),
        ]

        logging.basicConfig(
            handlers=handlers,
            format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG,
        )
        logging.captureWarnings(capture=True)

        # Log the initialization
        logger = logging.getLogger(__name__)
        logger.info(f"Logging initialized. Log file: {self.logs_dir.joinpath(log_file)}")

    def init_app_data(self):
        storage = self._db_from_current_user_project()
        self.app_data_reader = AppDataReader(storage.db)
        self.app_data_writer = AppDataWriter(storage.db)
        self.app_data_cache = AppDataCache(self.app_data_reader, self.app_data_writer)

    def new_app_data(self):
        """Used when a new project is created/opened and we just wanted to switch underlying
        db_table from AppDataReader and AppDataWriter without creating a new instance
        """
        storage = self._db_from_current_user_project()
        self.app_data_reader.ldb = storage.db
        self.app_data_writer.ldb = storage.db

    def save_window_state(self, geometry, window_state):
        self.settings.setValue(GEOMETRY_KEY, geometry)
        self.settings.setValue(WINDOW_STATE_KEY, window_state)
        self.settings.sync()

    def save_configuration(self, app_config: AppConfiguration):
        self.settings.setValue(STARTUP_CHECK_KEY, app_config.update_check_on_startup)
        self.settings.setValue(TLS_VERIFICATION_KEY, app_config.tls_verification)
        self.settings.setValue(ALLOW_REDIRECTS_KEY, app_config.allow_redirects)
        self.settings.setValue(HTTP_PROXY_KEY, app_config.http_proxy)
        self.settings.setValue(HTTPS_PROXY_KEY, app_config.https_proxy)
        self.settings.setValue(NO_PROXY_KEY, app_config.no_proxy)
        self.settings.setValue(REQUEST_TIMEOUT_SECS, app_config.timeout_in_secs)
        self.settings.setValue(PRINT_SHARE_SERVER, app_config.print_server)
        self.settings.sync()

    def load_configuration(self):
        app_config = AppConfiguration()
        app_config.update_check_on_startup = str_to_bool(
            self.settings.value(STARTUP_CHECK_KEY, AppConfiguration.update_check_on_startup),
        )
        app_config.tls_verification = str_to_bool(
            self.settings.value(TLS_VERIFICATION_KEY, AppConfiguration.tls_verification),
        )
        app_config.allow_redirects = str_to_bool(
            self.settings.value(ALLOW_REDIRECTS_KEY, AppConfiguration.allow_redirects),
        )
        app_config.http_proxy = self.settings.value(HTTP_PROXY_KEY, AppConfiguration.http_proxy)
        app_config.https_proxy = self.settings.value(HTTPS_PROXY_KEY, AppConfiguration.https_proxy)
        app_config.no_proxy = self.settings.value(NO_PROXY_KEY, AppConfiguration.no_proxy)
        app_config.timeout_in_secs = self.settings.value(REQUEST_TIMEOUT_SECS, AppConfiguration.timeout_in_secs)
        app_config.print_server = self.settings.value(PRINT_SHARE_SERVER, AppConfiguration.print_server)
        return app_config

    def geometry(self):
        return self.settings.value(GEOMETRY_KEY, None)

    def window_state(self):
        return self.settings.value(WINDOW_STATE_KEY, None)

    def save_current_project(self, user_project: UserProject):
        self.settings.setValue(CURRENT_PROJECT_LOCATION_KEY, user_project.location)
        self.settings.setValue(CURRENT_PROJECT_STATE_KEY, user_project.state)
        self.settings.sync()

    def load_current_project(self):
        current_project_location = self.settings.value(CURRENT_PROJECT_LOCATION_KEY, None)

        if not current_project_location:
            return self.create_new_project()

        return UserProject(
            location=current_project_location,
            state=self.settings.value(CURRENT_PROJECT_STATE_KEY),
        )

    def create_new_project(self):
        user_project = UserProject(
            location=self.docs_location.joinpath(random_project_name()).as_posix(),
            state=SavedState.UN_SAVED,
        )
        self.save_current_project(user_project)
        return user_project

    def _db_from_current_user_project(self):
        user_project: UserProject = self.load_current_project()
        data_location = user_project.location
        return Storage(data_location)


app_settings = CoreSettings()
