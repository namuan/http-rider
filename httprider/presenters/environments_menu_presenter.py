import json
from pathlib import Path
from typing import TYPE_CHECKING

import cattr

from httprider.core.core_settings import app_settings
from httprider.core.environment_interactor import environment_interactor
from httprider.model.app_data import Environment

if TYPE_CHECKING:
    from httprider.model.user_data import UserProject


class EnvironmentMenuPresenter:
    def __init__(self, parent):
        self.main_window = parent

    def on_export(self):
        user_project: UserProject = app_settings.load_current_project()
        current_project_folder = Path(user_project.location).parent
        file_location, _ = self.main_window.save_file(
            "Export Environments",
            current_project_folder,
            file_filter="Environment Files (*.envs.json)",
        )
        if file_location:
            envs: list[Environment] = app_settings.app_data_reader.get_environments_from_db()
            envs_json = cattr.unstructure(envs)
            Path(file_location).write_text(json.dumps(envs_json))

    def on_import(self):
        user_project: UserProject = app_settings.load_current_project()
        current_project_folder = Path(user_project.location).parent
        file_location, _ = self.main_window.open_file(
            "Import Environments",
            current_project_folder,
            file_filter="Environment Files (*.envs.json)",
        )
        if file_location:
            envs_raw_json = Path(file_location).read_text()
            envs_json = json.loads(envs_raw_json)
            envs: list[Environment] = cattr.structure(envs_json, list[Environment])
            for env in envs:
                environment_interactor.add_environment(env)

            app_settings.app_data_writer.signals.environments_imported.emit()
