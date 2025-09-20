from PyQt6.QtWidgets import QDialog

from httprider.generated.configuration_dialog import Ui_Configuration
from httprider.presenters import ConfigPresenter


class ConfigurationDialog(QDialog, Ui_Configuration):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.presenter = ConfigPresenter(self, parent)

    def initialize(self):
        self.setupUi(self)
        # @todo: Add validator
        # https://snorfalorpagus.net/blog/2014/08/09/validating-user-input-in-pyqt4-using-qvalidator/

    def show_dialog(self):
        self.presenter.load_configuration_dialog()
