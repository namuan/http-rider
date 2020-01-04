import darkdetect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import qApp


def is_dark():
    return darkdetect.isDark()


def light_palette():
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
    return palette


def dark_palette():
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
    return palette


def configure_theme(application):
    # palette = dark_palette() if is_dark() else light_palette()
    # theme_mode = "dark" if is_dark() else "light"
    # application.setStyle(Theme(palette))
    # application.style().load_stylesheet(theme_mode)

    current_font: QFont = application.font()
    current_font.setPointSize(12)
    application.setFont(current_font)
