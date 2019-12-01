import os
import shutil

from httprider.core.core_settings import app_settings
from httprider.model.user_data import UserProject, SavedState


class FileMenuPresenter:
    def __init__(self, parent):
        self.main_window = parent

    def on_file_new(self):
        app_settings.create_new_project()
        self.reload_app()

    def on_file_open(self):
        user_project: UserProject = app_settings.load_current_project()
        current_project_folder = os.path.dirname(user_project.location)
        file_location, _ = self.main_window.open_file(
            "Select Project File",
            current_project_folder,
            file_filter="Project Files (*.db)",
        )
        if file_location and file_location != user_project.location:
            user_project.location = file_location
            user_project.state = SavedState.SAVED
            app_settings.save_current_project(user_project)
            self.reload_app()

    def on_file_save(self, retain_current_project_file=False):
        user_project: UserProject = app_settings.load_current_project()
        current_project_folder = os.path.dirname(user_project.location)
        if user_project.state == SavedState.UN_SAVED:
            file_location, _ = self.main_window.save_file(
                "Save Project File",
                current_project_folder,
                file_filter="Project Files (*.db)",
            )
            if file_location and file_location != user_project.location:
                if retain_current_project_file:
                    shutil.copy(user_project.location, file_location)
                else:
                    shutil.move(user_project.location, file_location)
                user_project.location = file_location

            user_project.state = SavedState.SAVED
            app_settings.save_current_project(user_project)
            self.reload_app()
        else:
            self.main_window.request_presenter.update_current_api_call()

    def on_file_save_as(self):
        user_project: UserProject = app_settings.load_current_project()
        user_project.state = SavedState.UN_SAVED
        app_settings.save_current_project(user_project)
        self.on_file_save(retain_current_project_file=True)

    def reload_app(self):
        """Switches the underlying data table to point to new file
        And refreshes all the views"""
        app_settings.new_app_data()
        self.main_window.presenter.refresh_app()
