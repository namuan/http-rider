from PyQt6.QtWidgets import QDialog

from httprider.generated.environment_configuration_dialog import Ui_EnvironmentsConfigurationDialog
from httprider.presenters import EnvironmentConfigurationPresenter


class EnvironmentConfigurationDialog(QDialog, Ui_EnvironmentsConfigurationDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = EnvironmentConfigurationPresenter(self)

    def show_dialog(self):
        self.presenter.load_configuration_dialog()
