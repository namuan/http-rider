from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QListWidgetItem

from httprider.presenters import KeyValueListPresenter
from httprider.core.core_settings import app_settings
from httprider.model.app_data import ProjectInfo, TagInfo, COMMON_HEADERS, HTTP_CONTENT_TYPES
from httprider.widgets.tag_info_widget import TagInfoWidget


class ProjectInfoPresenter:
    def __init__(self, parent):
        self.parent_view = parent
        self.parent_view.finished.connect(self.on_close)

        self.parent_view.btn_add_server.pressed.connect(self.on_add_new_server)
        self.parent_view.btn_remove_server.pressed.connect(
            self.on_remove_selected_server
        )

        self.common_header_list_presenter = KeyValueListPresenter(
            self.parent_view.lst_common_headers,
            self,
            key_completions=COMMON_HEADERS,
            value_completions=HTTP_CONTENT_TYPES,
        )

        app_settings.app_data_writer.signals.api_call_tag_added.connect(
            self.on_tag_added
        )
        app_settings.app_data_writer.signals.api_call_tag_removed.connect(
            self.reload_tags
        )
        app_settings.app_data_writer.signals.api_call_removed.connect(self.reload_tags)
        app_settings.app_data_writer.signals.multiple_api_calls_added.connect(
            self.reload_tags
        )

    def show_dialog(self):
        project: ProjectInfo = app_settings.app_data_reader.get_or_create_project_info()
        self.parent_view.txt_project_title.setText(project.title)
        self.parent_view.txt_project_version.setText(project.version)
        self.parent_view.txt_project_info.setPlainText(project.info)
        self.parent_view.txt_tos_url.setText(project.tos_url)
        self.parent_view.txt_contact_name.setText(project.contact_name)
        self.parent_view.txt_contact_email.setText(project.contact_email)
        self.parent_view.txt_license_url.setText(project.license_url)
        self.parent_view.txt_license_name.setText(project.license_name)

        self.parent_view.lst_project_tags.clear()
        for t in sorted(project.tags, key=lambda ti: ti.name):
            self.add_tag_info_widget(t)

        self.parent_view.lst_servers.clear()
        for server in project.servers:
            self.add_widget_item(server)

        self.common_header_list_presenter.update_items(project.common_headers)

        self.parent_view.show()

    def on_add_new_server(self):
        selected_item = self.parent_view.lst_servers.currentItem()
        if not selected_item:
            self.add_widget_item("http://127.0.0.1:8000")
            return

        self.add_widget_item(selected_item.text())

    def on_remove_selected_server(self):
        selected_row = self.parent_view.lst_servers.currentRow()
        self.parent_view.lst_servers.takeItem(selected_row)

    def add_widget_item(self, server):
        item = QtWidgets.QListWidgetItem()
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        item.setText(server)
        self.parent_view.lst_servers.addItem(item)

    def on_tag_added(self, _, tag_name):
        project: ProjectInfo = app_settings.app_data_reader.get_or_create_project_info()
        if not any(ti for ti in project.tags if ti.name == tag_name):
            project.tags.append(TagInfo(name=tag_name))
        app_settings.app_data_writer.update_project_info(project)

    def reload_tags(self):
        api_calls = app_settings.app_data_cache.filter_api_calls()
        all_tags = {tag_name for api in api_calls for tag_name in api.tags}
        project: ProjectInfo = app_settings.app_data_reader.get_or_create_project_info()
        project.tags = [TagInfo(name=tag_name) for tag_name in all_tags]
        app_settings.app_data_writer.update_project_info(project)

    def add_tag_info_widget(self, tag_info):
        item = QListWidgetItem()
        ti_widget = TagInfoWidget(self.parent_view.lst_project_tags)
        ti_widget.setData(tag_info)
        item.setSizeHint(ti_widget.minimumSizeHint())
        self.parent_view.lst_project_tags.addItem(item)
        self.parent_view.lst_project_tags.setItemWidget(item, ti_widget)

    def get_tags(self):
        tags = []
        for i in range(self.parent_view.lst_project_tags.count()):
            item = self.parent_view.lst_project_tags.item(i)
            widget = self.parent_view.lst_project_tags.itemWidget(item)
            tag_info = widget.getData()
            tags.append(tag_info)
        return tags

    def get_servers(self):
        servers = []
        for i in range(self.parent_view.lst_servers.count()):
            item = self.parent_view.lst_servers.item(i)
            servers.append(item.text())
        return servers

    def get_common_headers(self):
        return self.common_header_list_presenter.get_items()

    def on_close(self):
        project: ProjectInfo = app_settings.app_data_reader.get_or_create_project_info()
        project.title = self.parent_view.txt_project_title.text()
        project.version = self.parent_view.txt_project_version.text()
        project.info = self.parent_view.txt_project_info.toPlainText()
        project.tos_url = self.parent_view.txt_tos_url.text()
        project.contact_name = self.parent_view.txt_contact_name.text()
        project.contact_email = self.parent_view.txt_contact_email.text()
        project.license_url = self.parent_view.txt_license_url.text()
        project.license_name = self.parent_view.txt_license_name.text()

        project.tags = self.get_tags()
        project.servers = self.get_servers()
        project.common_headers = self.get_common_headers()

        app_settings.app_data_writer.update_project_info(project)
