from PyQt6.QtWidgets import QDialog

from httprider.generated.assertion_builder_dialog import Ui_AssertionBuilderDialog
from httprider.presenters.assertion_builder_presenter import AssertionBuilderPresenter


class AssertionBuilderDialog(QDialog, Ui_AssertionBuilderDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = AssertionBuilderPresenter(self)

    def show_dialog(self, api_call):
        self.presenter.load_configuration_dialog(api_call)
