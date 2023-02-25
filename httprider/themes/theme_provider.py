from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon, QFont, QFontDatabase

from httprider.core.theme_mode import is_dark
from httprider.themes.theme import Theme


def configure_theme(application):
    application.setWindowIcon(QIcon(":/icons/httprider.ico"))

    application.setStyle(Theme())
    theme_mode = "dark" if is_dark() else "light"
    application.style().load_stylesheet(theme_mode)

    font_db = QFontDatabase()
    font_db.addApplicationFont(":/fonts/JetBrainsMono-Regular.ttf")

    current_font: QFont = QFont("JetBrains Mono")
    current_font.setPointSize(12)
    application.setFont(current_font)


def api_call_separator_rect():
    return QColor("#404040") if is_dark() else QColor("#404040")


def api_call_list_selected_rect():
    return QColor("#505153") if is_dark() else QColor("#CBD8E1")


def api_call_list_selected_pen():
    return Qt.GlobalColor.white if is_dark() else Qt.GlobalColor.black


def api_call_list_title_color():
    return Qt.GlobalColor.white if is_dark() else Qt.GlobalColor.black


def api_call_list_sub_title_color():
    return Qt.GlobalColor.white if is_dark() else Qt.GlobalColor.black


def api_call_list_disabled_color():
    return QColor("#343434") if is_dark() else QColor("#cfd2d6")


def api_call_list_disabled_title_color():
    return Qt.darkGray if is_dark() else Qt.gray


def api_call_list_disabled_sub_title_color():
    return Qt.darkGray if is_dark() else Qt.gray


def api_call_list_status_code_color():
    return Qt.GlobalColor.white if is_dark() else Qt.GlobalColor.white


def http_ex_success():
    return QColor("#01721d") if is_dark() else QColor("#01721d")


def http_ex_client_err():
    return QColor("#d8a413") if is_dark() else QColor("#d8a413")


def http_ex_server_err():
    return QColor("#a51e00") if is_dark() else QColor("#a51e00")


def http_ex_no_response():
    return QColor("#a51e00") if is_dark() else QColor("#a51e00")
