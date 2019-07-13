from PyQt5 import QtWidgets, QtGui

from ..model.app_data import ApiCall


class ApiCallWidget(QtWidgets.QWidget):
    doc_id: int

    def __init__(self, parent=None):
        super(ApiCallWidget, self).__init__(parent)
        self.vertical_layout = QtWidgets.QVBoxLayout()

        self.lbl_title = QtWidgets.QLabel()
        self.lbl_http_request = QtWidgets.QLabel()

        self.vertical_layout.addWidget(self.lbl_title)
        self.vertical_layout.addWidget(self.lbl_http_request)

        self.setLayout(self.vertical_layout)

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.lbl_title.setFont(font)

    def set_data(self, doc_id, api_call: ApiCall):
        self.doc_id = doc_id
        self.lbl_title.setText(api_call.title)
        self.lbl_http_request.setText(f"{api_call.http_method} {api_call.http_url}")
        self.setToolTip(api_call.description)

    def get_data(self):
        return self.doc_id
