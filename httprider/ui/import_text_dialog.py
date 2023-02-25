from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog

from ..generated.import_text_dialog import Ui_ImportTextDialog


class ImportTextDialog(QDialog, Ui_ImportTextDialog):
    accepted_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.import_function = None

    def accept(self):
        if self.import_function:
            try:
                _, api_calls = self.import_function(self.txt_import.toPlainText())
                self.accepted_signal.emit(api_calls)
                super().accept()
            except SyntaxError as e:
                self.lbl_error_message.setText(e.msg)

    def show_dialog(self, import_funcion):
        self.import_function = import_funcion
        self.lbl_error_message.clear()
        self.show()
