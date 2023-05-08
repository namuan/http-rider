from PyQt6.QtWidgets import QDialog

from ..generated.fuzz_test_dialog import Ui_FuzzTestDialog
from ..presenters import FuzzTestPresenter


class FuzzTestDialog(QDialog, Ui_FuzzTestDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = FuzzTestPresenter(self, parent)

    def fuzz_single_dialog(self):
        self.presenter.show_dialog()
