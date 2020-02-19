from PyQt5.QtWidgets import QDialog

from httprider.generated.openapi_sdk_gen_dialog import Ui_OpenApiSdkDialog
from httprider.presenters import OpenApiSdkGeneratorPresenter


class OpenApiGeneratorDialog(QDialog, Ui_OpenApiSdkDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = OpenApiSdkGeneratorPresenter(self, parent)

    def show_dialog(self):
        self.presenter.show_dialog()
