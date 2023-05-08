from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog

from ..presenters.utility_functions_presenter import UtilityFunctionsPresenter
from ..generated.tools_dialog import Ui_UtilityFunctionsDialog


class UtilityFunctionsDialog(QDialog, Ui_UtilityFunctionsDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowType.Popup | QtCore.Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(self.size())

        self.presenter = UtilityFunctionsPresenter(self, parent)

    def exec_dialog(self):
        self.presenter.init()
        return self.exec()

    def get_function(self):
        return self.presenter.get_function()
