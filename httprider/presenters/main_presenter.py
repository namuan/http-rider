import logging

from ..core.core_settings import app_settings
from ..core.worker_pool import single_worker


class MainPresenter:
    def __init__(self, view):
        self.view = view
        self.initial_load = True
        app_settings.init()
        app_settings.init_logger()
        app_settings.init_app_data()
        if app_settings.geometry():
            self.view.restoreGeometry(app_settings.geometry())
        if app_settings.window_state():
            self.view.restoreState(app_settings.window_state())
        app_settings.app_data_writer.signals.api_call_added.connect(self.show_frame)
        app_settings.app_data_writer.signals.api_call_removed.connect(self.show_frame)
        app_settings.app_data_writer.signals.multiple_api_calls_added.connect(self.show_frame)

    def after_window_loaded(self):
        if not self.initial_load:
            return

        self.initial_load = False
        self.refresh_app()
        self.check_updates()

    def refresh_app(self):
        app_settings.app_data_cache.load_cache()
        self.show_frame()
        self.view.refresh_all_views()
        current_project = app_settings.load_current_project()
        window_title = f"{current_project.location}"
        self.view.setWindowTitle(window_title)

    def show_frame(self):
        api_calls = app_settings.app_data_cache.filter_api_calls()
        if api_calls:
            logging.info(f"API Calls found: {len(api_calls)}. Hiding Empty Frame")
            self.view.empty_frame.hide()
            self.view.frame_request_response.show()
            self.view.frame_exchange.show()
        else:
            logging.info(f"API Calls found: {len(api_calls)}. Showing Empty Frame")
            self.view.empty_frame_presenter.display()
            self.view.request_presenter.cleanup()
            self.view.exchange_presenter.cleanup()

    def check_updates(self):
        if app_settings.load_updates_configuration():
            self.view.updater.check()

    def save_settings(self):
        logging.info("Saving settings for Main Window")
        app_settings.save_window_state(
            geometry=self.view.saveGeometry(),
            window_state=self.view.saveState()
        )

    def shutdown(self):
        single_worker.shutdown()
        self.save_settings()
