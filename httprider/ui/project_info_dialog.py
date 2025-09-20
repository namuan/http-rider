from PyQt6.QtWidgets import QDialog

from httprider.generated.project_info_dialog import Ui_ProjectInfoDialog
from httprider.presenters.project_info_presenter import ProjectInfoPresenter


class ProjectInfoDialog(QDialog, Ui_ProjectInfoDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = ProjectInfoPresenter(self)

    def show_dialog(self):
        self.presenter.show_dialog()
