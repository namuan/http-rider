import logging

from httprider.core import gen_uuid
from httprider.core.core_settings import app_settings
from httprider.model.app_data import Environment


class EnvironmentInteractor:

    def add_environment(self, environment: Environment):
        environment.id = gen_uuid()
        app_settings.app_data_writer.update_environment_in_db(environment)
        logging.info(f"Environment Added :: {environment.id} -> {environment}")
        app_settings.app_data_writer.signals.environment_added.emit(environment.id)
        return environment.id

    def remove_environment(self, environment_name):
        app_settings.app_data_writer.remove_environment_from_db(environment_name)
        app_settings.app_data_writer.signals.environment_removed.emit()

    def update_environment_name(self, old_environment_name, new_environment):
        app_settings.app_data_writer.update_environment_name_in_db(old_environment_name, new_environment)
        app_settings.app_data_writer.signals.environment_renamed.emit()

    def update_environment_data(self, environment_name, environment_data):
        environment: Environment = app_settings.app_data_cache.get_selected_environment(environment_name)
        environment.set_data(environment_data)
        app_settings.app_data_writer.update_environment_in_db(environment)
        app_settings.app_data_writer.signals.environment_data_changed.emit(environment_name)


environment_interactor = EnvironmentInteractor()
