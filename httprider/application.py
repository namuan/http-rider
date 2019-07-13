import sys

from PyQt5.QtWidgets import *

from . import __version__, __appname__, __desktopid__
from .themes.light_theme import LightTheme
from .ui.main_window import MainWindow


def configure_theme(application):
    application.setStyle(LightTheme())
    application.style().load_stylesheet()


def main():
    application = QApplication(sys.argv)
    application.setApplicationVersion(__version__)
    application.setApplicationName(__appname__)
    application.setDesktopFileName(__desktopid__)

    window = MainWindow()
    configure_theme(application)

    window.show()
    sys.exit(application.exec_())
