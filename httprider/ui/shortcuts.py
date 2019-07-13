from PyQt5.QtGui import *
from PyQt5.QtWidgets import QShortcut


def shortcut_items(self):
    http_url = QShortcut(QKeySequence("Ctrl+L"), self)
    http_url.activated.connect(self.empty_frame_presenter.focus_http_url)

    http_method = QShortcut(QKeySequence("Ctrl+M"), self)
    http_method.activated.connect(self.empty_frame_presenter.focus_http_method)

    description = QShortcut(QKeySequence("Alt+D"), self)
    description.activated.connect(self.empty_frame_presenter.focus_description)

    headers = QShortcut(QKeySequence("Alt+H"), self)
    headers.activated.connect(self.empty_frame_presenter.focus_headers)

    query_params = QShortcut(QKeySequence("Alt+Q"), self)
    query_params.activated.connect(self.empty_frame_presenter.focus_query_params)

    form_params = QShortcut(QKeySequence("Alt+F"), self)
    form_params.activated.connect(self.empty_frame_presenter.focus_form_params)

    request_body = QShortcut(QKeySequence("Alt+B"), self)
    request_body.activated.connect(self.empty_frame_presenter.focus_request_body)

    prev_request = QShortcut(QKeySequence("Ctrl+Up"), self)
    prev_request.activated.connect(self.api_list_presenter.selectPreviousApiCall)

    next_request = QShortcut(QKeySequence("Ctrl+Down"), self)
    next_request.activated.connect(self.api_list_presenter.selectNextApiCall)
