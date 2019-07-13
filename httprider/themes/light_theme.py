import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QProxyStyle, qApp

from ..core import styles_from_file


class LightTheme(QProxyStyle):
    def __init__(self):
        super(LightTheme, self).__init__()
        palette = qApp.palette()
        palette.setColor(QPalette.Window, QColor(239, 240, 241))
        palette.setColor(QPalette.WindowText, QColor(49, 54, 59))
        palette.setColor(QPalette.Base, QColor(252, 252, 252))
        palette.setColor(QPalette.AlternateBase, QColor(239, 240, 241))
        palette.setColor(QPalette.ToolTipBase, QColor(239, 240, 241))
        palette.setColor(QPalette.ToolTipText, QColor(49, 54, 59))
        palette.setColor(QPalette.Text, QColor(49, 54, 59))
        palette.setColor(QPalette.Button, QColor(239, 240, 241))
        palette.setColor(QPalette.ButtonText, QColor(49, 54, 59))
        palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
        palette.setColor(QPalette.Link, QColor(41, 128, 185))
        palette.setColor(QPalette.Highlight, QColor(126, 71, 130))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        palette.setColor(QPalette.Disabled, QPalette.Light, Qt.white)
        palette.setColor(QPalette.Disabled, QPalette.Shadow, QColor(234, 234, 234))
        qApp.setPalette(palette)

    def load_stylesheet(self):
        filename = ":/themes/light.qss"

        styles = styles_from_file(filename)
        qApp.setStyleSheet(styles) if styles else self.log_error(filename)

    def log_error(self, styles_file):
        logging.error(f"Unable to read file from {styles_file}")
