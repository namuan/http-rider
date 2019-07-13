import logging

from ..core.core_settings import app_settings


class ConfigPresenter:
    def __init__(self, view, parent_view):
        self.view = view
        self.parent_view = parent_view
        self.view.initialize()
        self.view.btn_save_configuration.pressed.connect(self.on_success)
        self.view.btn_cancel_configuration.pressed.connect(self.ignore_changes)

    def ignore_changes(self):
        self.view.reject()

    def on_success(self):
        logging.info("Saving configuration")
        updates_check = self.view.chk_updates_startup.isChecked()
        app_settings.save_configuration(updates_check)
        self.parent_view.status_bar.showMessage("Ready", 5000)
        self.view.accept()

    def load_configuration_dialog(self):
        check_updates = app_settings.load_updates_configuration()
        self.view.chk_updates_startup.setChecked(check_updates)
        self.view.show()
