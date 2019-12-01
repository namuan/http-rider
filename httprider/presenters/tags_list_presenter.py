from httprider.core.app_state_interactor import AppStateInteractor
from httprider.core.constants import *
from httprider.core.core_settings import app_settings


class TagsListPresenter:
    def __init__(self, parent_view=None):
        self.parent_view = parent_view
        self.app_state_interactor = AppStateInteractor()
        app_settings.app_data_writer.signals.project_info_updated.connect(self.refresh)

    def __get_combox_box(self):
        toolbar_actions = self.parent_view.tool_bar.actions()
        tags_list_action = next(act for act in toolbar_actions if act.text() == "Tags")
        return tags_list_action.defaultWidget()

    def on_tag_changed(self, tag_name):
        self.app_state_interactor.update_selected_tag(tag_name)

    def refresh(self):
        project_info = app_settings.app_data_reader.get_or_create_project_info()
        tags_list_field = self.__get_combox_box()
        selected_tag = tags_list_field.currentText()
        tags_list_field.clear()
        tags_list_field.addItem(DEFAULT_TAG)
        for tag in project_info.tags:
            tags_list_field.addItem(tag.name)

        tags_list_field.setCurrentText(selected_tag)
