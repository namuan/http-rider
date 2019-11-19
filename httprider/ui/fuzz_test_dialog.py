from PyQt5.QtWidgets import QDialog

from ..generated.fuzz_test_dialog import Ui_FuzzTestDialog
from ..presenters import FuzzTestPresenter
from ..presenters.fuzz_test_presenter import DisplayMode


class FuzzTestDialog(QDialog, Ui_FuzzTestDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = FuzzTestPresenter(self, parent)

    def export_single_dialog(self):
        self.presenter.mode = DisplayMode.SINGLE_API
        self.presenter.show_dialog()

    def export_all_dialog(self):
        self.presenter.mode = DisplayMode.MULTIPLE_APIS
        self.presenter.show_dialog()
