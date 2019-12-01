import logging

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from httprider.core.environment_interactor import environment_interactor
from httprider.core import random_environment
from httprider.core.core_settings import app_settings
from httprider.model.app_data import Environment
from httprider.presenters import KeyValueListPresenter


class EnvironmentConfigurationPresenter:
    def __init__(self, parent_view):
        self.initial_load = True
        self.selected_environment = None
        self.parent_view = parent_view
        self.environment_data_presenter = KeyValueListPresenter(
            self.parent_view.lst_environment_data, self
        )

        # domain events
        app_settings.app_data_reader.signals.initial_cache_loading_completed.connect(
            self.refresh
        )

        # ui events
        self.parent_view.finished.connect(self.on_close)
        self.parent_view.lst_environments.currentItemChanged.connect(
            self.on_current_item_changed
        )
        self.parent_view.btn_add_environment.pressed.connect(
            self.on_add_new_environment
        )
        self.parent_view.btn_remove_environment.pressed.connect(
            self.on_remove_selected_environment
        )
        self.parent_view.btn_duplicate_environment.pressed.connect(
            self.on_duplicate_environment
        )
        self.parent_view.lst_environments.itemChanged.connect(self.on_item_changed)
        self.parent_view.lst_environments.itemSelectionChanged.connect(
            self.on_item_selection_changed
        )

    def refresh(self):
        self.parent_view.lst_environments.clear()
        self.environment_data_presenter.clear()
        environments = app_settings.app_data_cache.get_environments()
        logging.info(
            f"Refreshing env config :: Total environments: {len(environments)}"
        )
        for environment in environments:
            self.__add_environment_widget_item(environment)

        if environments:
            self.parent_view.lst_environments.setCurrentRow(0)

    def on_duplicate_environment(self):
        selected_item = self.parent_view.lst_environments.currentItem()
        if not selected_item:
            return

        new_env_name = random_environment()
        logging.info(
            f"Environment Duplicated :: {selected_item.text()} -> {new_env_name}"
        )
        selected_environment = app_settings.app_data_cache.get_selected_environment(
            selected_item.text()
        )
        selected_environment.name = new_env_name
        self.__add_environment_widget_item(selected_environment)
        environment_interactor.add_environment(selected_environment)

    def on_add_new_environment(self):
        new_env = Environment(name=random_environment(), data={})
        self.__add_environment_widget_item(new_env)
        environment_interactor.add_environment(new_env)
        self.parent_view.lst_environments.setCurrentRow(
            self.parent_view.lst_environments.count() - 1
        )

    def on_remove_selected_environment(self):
        current_row = self.parent_view.lst_environments.currentRow()
        selected_item = self.parent_view.lst_environments.item(current_row)
        if not selected_item:
            return

        selected_environment = selected_item.text()
        self.parent_view.lst_environments.takeItem(current_row)
        logging.info(f"Removing selected environment: {selected_environment}")
        environment_interactor.remove_environment(selected_environment)

    def on_current_item_changed(self, newly_selected_item, previous_selected_item):
        if not newly_selected_item:
            return

        newly_selected_environment = newly_selected_item.text()
        logging.debug(f"on_item_selection_changed: {newly_selected_environment}")

        if previous_selected_item:
            previously_selected_item_text = previous_selected_item.text()
            logging.debug(
                f"saving previously selected item: {previously_selected_item_text}"
            )
            self.__save_environment_data(previously_selected_item_text)

        env = app_settings.app_data_cache.get_selected_environment(
            newly_selected_environment
        )
        if env and env.get_data():
            logging.debug(f"Env: {env.name} has data {env.get_data()}")
            self.environment_data_presenter.update_items(env.get_data())
            self.set_selected_environment(newly_selected_environment)
        else:
            self.environment_data_presenter.clear()

    def on_item_selection_changed(self):
        newly_selected_item = self.parent_view.lst_environments.currentItem()
        if not newly_selected_item:
            return

        self.set_selected_environment(newly_selected_item.text())

    def set_selected_environment(self, new_environment=None):
        logging.debug(
            f"Setting selected environment from: {self.selected_environment} to {new_environment}"
        )
        self.selected_environment = new_environment

    def on_item_changed(self, changed_item):
        old_environment_name = self.selected_environment
        changed_environment_name = changed_item.text()
        old_environment: Environment = app_settings.app_data_cache.get_selected_environment(
            old_environment_name
        )
        old_environment.name = changed_environment_name

        logging.debug(
            f"==== on_item_changed: {changed_environment_name} from {old_environment_name}"
        )
        environment_interactor.update_environment_name(
            old_environment_name, old_environment
        )
        self.set_selected_environment(changed_environment_name)

    def load_configuration_dialog(self):
        if not self.initial_load:
            return self.parent_view.show()
        else:
            self.initial_load = False

        environments = app_settings.app_data_cache.get_environments()
        if not environments:
            self.__default_data_setup()
        else:
            self.refresh()

        self.parent_view.lst_environments.setCurrentRow(0)
        self.parent_view.show()

    def on_close(self):
        selected_item = self.parent_view.lst_environments.currentItem()
        if not selected_item:
            return
        self.__save_environment_data(selected_item.text())

    def __save_environment_data(self, environment_name):
        environment_data = self.environment_data_presenter.get_items()
        environment_interactor.update_environment_data(
            environment_name, environment_data
        )

    def __add_environment_widget_item(self, env: Environment):
        item = QtWidgets.QListWidgetItem()
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setText(env.name)
        self.parent_view.lst_environments.addItem(item)

    def __default_data_setup(self):
        default_env = Environment(name="Default")
        default_env.add_data("API_URL", "http://127.0.0.1:8000")
        self.__add_environment_widget_item(default_env)
        environment_interactor.add_environment(default_env)
