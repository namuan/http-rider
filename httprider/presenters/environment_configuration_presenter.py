from PyQt5 import QtCore
from PyQt5 import QtWidgets

from ..core import random_environment
from ..core.core_settings import app_settings
from ..model.app_data import Environment
from ..presenters import KeyValueListPresenter


class EnvironmentConfigurationPresenter:
    def __init__(self, parent_view):
        self.initial_load = True
        self.parent_view = parent_view
        self.parent_view.finished.connect(self.on_close)
        self.parent_view.btn_add_environment.pressed.connect(self.on_add_new_environment)
        self.parent_view.btn_remove_environment.pressed.connect(self.on_remove_selected_environment)
        self.parent_view.lst_environments.itemChanged.connect(self.on_item_changed)
        self.parent_view.lst_environments.itemSelectionChanged.connect(self.on_item_selection_changed)
        self.parent_view.btn_duplicate_environment.pressed.connect(self.on_duplicate_environment)
        self.environment_data_presenter = KeyValueListPresenter(self.parent_view.lst_environment_data, self)
        self.selected_environment = None
        app_settings.app_data_writer.signals.environment_added.connect(self.refresh)
        app_settings.app_data_writer.signals.environment_removed.connect(self.refresh)

    def refresh(self):
        self.parent_view.lst_environments.clear()
        environments = app_settings.app_data_reader.get_environments()
        for environment in environments:
            self.__add_environment_widget_item(environment)
        self.parent_view.lst_environments.setCurrentRow(
            self.parent_view.lst_environments.count() - 1
        )

    def on_duplicate_environment(self):
        selected_item = self.parent_view.lst_environments.currentItem()
        if not selected_item:
            return
        new_env_name = random_environment()
        selected_environment = app_settings.app_data_reader.get_selected_environment(
            selected_item.text()
        )
        selected_environment.name = new_env_name
        app_settings.app_data_writer.add_environment(selected_environment)

    def on_add_new_environment(self):
        new_env = Environment(name=random_environment())
        app_settings.app_data_writer.add_environment(new_env)

    def on_remove_selected_environment(self):
        selected_item = self.parent_view.lst_environments.currentItem()
        # selected_item = self.parent_view.lst_environments.takeItem(selected_row)
        app_settings.app_data_writer.remove_environment(selected_item.text())

    def on_item_selection_changed(self):
        newly_selected_item = self.parent_view.lst_environments.currentItem()
        if not newly_selected_item:
            return

        # Checking for last selected environment
        # So we can persist any modifications before switching over
        # to the new environment
        if self.selected_environment:
            self.__save_environment_data(self.selected_environment)

        newly_selected_environment = newly_selected_item.text()
        env = app_settings.app_data_reader.get_selected_environment(newly_selected_environment)
        self.environment_data_presenter.update_items(env.data)
        self.selected_environment = newly_selected_environment

    def on_item_changed(self, item):
        app_settings.app_data_writer.update_environment_name(self.selected_environment, item.text())
        self.selected_environment = item.text()

    def load_configuration_dialog(self):
        if not self.initial_load:
            return self.parent_view.show()
        else:
            self.initial_load = False

        environments = app_settings.app_data_reader.get_environments()
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
        app_settings.app_data_writer.update_environment_data(environment_name, environment_data)

    def __add_environment_widget_item(self, env: Environment):
        item = QtWidgets.QListWidgetItem()
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setText(env.name)
        self.parent_view.lst_environments.addItem(item)

    def __default_data_setup(self):
        default_env = Environment(name="Default")
        default_env.add_data("API_URL", "http://127.0.0.1:8000")
        app_settings.app_data_writer.add_environment(default_env)
