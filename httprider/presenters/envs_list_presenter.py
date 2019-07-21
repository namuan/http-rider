from httprider.core.app_state_interactor import AppStateInteractor
from ..core.core_settings import app_settings


class EnvironmentsListPresenter:
    def __init__(self, parent_view=None):
        self.parent_view = parent_view
        self.app_state_interactor = AppStateInteractor()
        app_settings.app_data_writer.signals.environment_added.connect(self.refresh)
        app_settings.app_data_writer.signals.environment_removed.connect(self.refresh)
        app_settings.app_data_writer.signals.environment_renamed.connect(self.refresh)

    def __get_combox_box(self):
        toolbar_actions = self.parent_view.tool_bar.actions()
        tags_list_action = next(act for act in toolbar_actions if act.text() == 'Environmnents')
        return tags_list_action.defaultWidget()

    def on_env_changed(self, new_env):
        self.app_state_interactor.update_selected_environment(new_env)

    def refresh(self):
        all_envs = app_settings.app_data_reader.get_environments()
        envs_list_field = self.__get_combox_box()
        selected_env = app_settings.app_data_reader.get_appstate_environment()
        envs_list_field.clear()
        for env in all_envs:
            envs_list_field.addItem(env.name)

        envs_list_field.setCurrentText(selected_env)
