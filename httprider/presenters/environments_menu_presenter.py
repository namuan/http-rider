import json
import os
from pathlib import Path

import cattr
from typing import List

from ..model.app_data import Environment
from ..core.core_settings import app_settings
from ..model.user_data import UserProject


class EnvironmentMenuPresenter:
    def __init__(self, parent):
        self.main_window = parent

    def on_export(self):
        user_project: UserProject = app_settings.load_current_project()
        current_project_folder = os.path.dirname(user_project.location)
        file_location, _ = self.main_window.save_file(
            "Export Environments",
            current_project_folder,
            file_filter="Environment Files (*.envs.json)",
        )
        if file_location:
            envs: List[
                Environment
            ] = app_settings.app_data_reader.get_environments_from_db()
            envs_json = cattr.unstructure(envs)
            Path(file_location).write_text(json.dumps(envs_json))

    def on_import(self):
        user_project: UserProject = app_settings.load_current_project()
        current_project_folder = os.path.dirname(user_project.location)
        file_location, _ = self.main_window.open_file(
            "Import Environments",
            current_project_folder,
            file_filter="Environment Files (*.envs.json)",
        )
        if file_location:
            envs_raw_json = Path(file_location).read_text()
            envs_json = json.loads(envs_raw_json)
            envs: List[Environment] = cattr.structure(envs_json, List[Environment])
            for env in envs:
                app_settings.app_data_writer.update_environment_in_db(env)

            app_settings.app_data_writer.signals.environment_added.emit("")
