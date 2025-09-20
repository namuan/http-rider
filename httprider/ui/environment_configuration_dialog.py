from PyQt6.QtWidgets import QDialog

from ..generated.environment_configuration_dialog import (
    Ui_EnvironmentsConfigurationDialog,
)
from ..presenters import EnvironmentConfigurationPresenter


class EnvironmentConfigurationDialog(QDialog, Ui_EnvironmentsConfigurationDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # self.setFixedSize(self.size())
        self.presenter = EnvironmentConfigurationPresenter(self)

    def show_dialog(self):
        self.presenter.load_configuration_dialog()
