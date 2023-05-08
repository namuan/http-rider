from PyQt6.QtWidgets import QDialog

from httprider.generated.code_generator_dialog import Ui_CodeGeneratorDialog
from httprider.presenters import CodeGeneratorPresenter
from httprider.presenters.code_generator_presenter import DisplayMode


class CodeGeneratorDialog(QDialog, Ui_CodeGeneratorDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = CodeGeneratorPresenter(self, parent)

    def export_single_dialog(self):
        self.presenter.mode = DisplayMode.SINGLE_API
        self.presenter.show_dialog()

    def export_all_dialog(self):
        self.presenter.mode = DisplayMode.MULTIPLE_APIS
        self.presenter.show_dialog()
