from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from httprider.core.theme_mode import is_dark
from httprider.themes.theme import Theme


def configure_theme(application):
    theme = Theme(application)
    theme_mode = "dark" if is_dark() else "light"
    theme.load_stylesheet(theme_mode)


def api_call_list_rect():
    return QColor("#2b2b2b") if is_dark() else QColor("#ffffff")


def api_call_list_pen():
    return Qt.GlobalColor.white if is_dark() else Qt.GlobalColor.black


def api_call_separator_rect():
    return QColor("#404040")


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
    return Qt.GlobalColor.darkGray if is_dark() else Qt.GlobalColor.gray


def api_call_list_disabled_sub_title_color():
    return Qt.GlobalColor.darkGray if is_dark() else Qt.GlobalColor.gray


def api_call_list_status_code_color():
    return Qt.GlobalColor.white


def http_ex_success():
    return QColor("#01721d")


def http_ex_client_err():
    return QColor("#d8a413")


def http_ex_server_err():
    return QColor("#a51e00")


def http_ex_no_response():
    return QColor("#a51e00")
