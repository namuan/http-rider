import sys

from PyQt5.QtWidgets import *

from httprider.themes import theme_provider
from httprider.ui.main_window import MainWindow
from . import __version__, __appname__, __desktopid__


def main():
    application = QApplication(sys.argv)
    application.setApplicationVersion(__version__)
    application.setApplicationName(__appname__)
    application.setDesktopFileName(__desktopid__)

    window = MainWindow()
    theme_provider.configure_theme(application)

    window.show()
    sys.exit(application.exec_())
