import logging

from ..core.core_settings import app_settings
from ..model.app_configuration import AppConfiguration


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
        app_config = self.form_to_object()
        app_settings.save_configuration(app_config)
        self.parent_view.status_bar.showMessage("Ready", 5000)
        self.view.accept()

    def load_configuration_dialog(self):
        app_config = app_settings.load_configuration()
        self.object_to_form(app_config)
        self.view.show()

    def form_to_object(self):
        config = AppConfiguration()
        config.update_check_on_startup = self.view.chk_updates_startup.isChecked()
        config.tls_verification = self.view.chk_tls_verficiation.isChecked()
        config.http_proxy = self.view.txt_http_proxy.text()
        config.https_proxy = self.view.txt_https_proxy.text()
        return config

    def object_to_form(self, app_config: AppConfiguration):
        self.view.chk_updates_startup.setChecked(app_config.update_check_on_startup)
        self.view.chk_tls_verficiation.setChecked(app_config.tls_verification)
        self.view.txt_http_proxy.setText(app_config.http_proxy)
        self.view.txt_https_proxy.setText(app_config.https_proxy)
