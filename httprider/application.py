import logging
import sys

from PyQt6.QtWidgets import *

from httprider import __appname__, __desktopid__, __version__
from httprider.core.core_settings import app_settings
from httprider.themes.theme_provider import configure_theme
from httprider.ui.main_window import MainWindow


def main():
    application = QApplication(sys.argv)
    application.setApplicationVersion(__version__)
    application.setApplicationName(__appname__)
    application.setDesktopFileName(__desktopid__)

    logging.info("Configuring application theme and stylesheets")
    configure_theme(application)

    # Initialize app settings
    app_settings.init()

    main_window = MainWindow()
    main_window.show()

    sys.exit(application.exec())
