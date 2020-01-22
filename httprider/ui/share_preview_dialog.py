from PyQt5.QtWidgets import QDialog

from httprider.generated.share_preview_dialog import Ui_SharePreviewDialog
from httprider.model.app_data import HttpExchange
from httprider.presenters import SharePreviewPresenter


class SharePreviewDialog(QDialog, Ui_SharePreviewDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = SharePreviewPresenter(self, parent)

    def show_exchange_preview(self, selected_exchange: HttpExchange):
        self.presenter.show_dialog(selected_exchange)

    def show_multiple_exchanges_preview(self):
        self.presenter.show_dialog_multiple_apis()
