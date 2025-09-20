from PyQt6 import QtCore
from PyQt6.QtWidgets import QDialog

from ..generated.faker_dialog import Ui_DataGeneratorDialog
from ..presenters.data_generator_presenter import DataGeneratorPresenter


class DataGeneratorDialog(QDialog, Ui_DataGeneratorDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(self.size())

        self.presenter = DataGeneratorPresenter(self, parent)

    def exec_dialog(self):
        self.presenter.fake_to_form()
        return self.exec()

    def get_function(self):
        return self.presenter.get_function()
