import logging

from httprider.core.core_settings import app_settings


class AppStateInteractor:

    def update_sequence_number(self):
        app_state = app_settings.app_data_cache.get_app_state()
        app_state.last_sequence_number = app_state.last_sequence_number + 1000
        logging.info(f"Updating to sequence number: {app_state.last_sequence_number}")
        app_settings.app_data_writer.update_app_state(app_state)
        return app_state.last_sequence_number

    def update_selected_tag(self, new_tag_name):
        if not new_tag_name:
            return

        app_state = app_settings.app_data_cache.get_app_state()
        if app_state.selected_tag != new_tag_name:
            logging.info(f"Selected tag changed to {new_tag_name}")
            app_state.selected_tag = new_tag_name
            app_settings.app_data_writer.update_app_state(app_state)
            app_settings.app_data_writer.signals.selected_tag_changed.emit(new_tag_name)

    def update_selected_environment(self, environment_name):
        logging.info(f"Selected environment changed to {environment_name}")
        app_state = app_settings.app_data_cache.get_app_state()
        app_state.selected_env = environment_name
        app_settings.app_data_writer.update_app_state(app_state)
        app_settings.app_data_writer.signals.selected_env_changed.emit(environment_name)
