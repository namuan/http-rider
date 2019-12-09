import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QKeyEvent
from PyQt5.QtWidgets import *

from httprider.core.api_call_interactor import api_call_interactor
from httprider.model.completer import get_completer_model
from httprider.presenters.mocked_response_presenter import MockedResponsePresenter
from httprider.core import styles_from_file, split_url_qs
from httprider.core.core_settings import app_settings
from httprider.core.safe_rest_api_interactor import rest_api_interactor
from httprider.exporters.common import api_request_body_highlighted
from httprider.model.app_data import ApiCall, COMMON_HEADERS, HTTP_CONTENT_TYPES
from httprider.presenters import AssertionResultPresenter, KeyValueListPresenter
from httprider.ui.assertion_builder_dialog import AssertionBuilderDialog
from httprider.widgets.completion_line_edit import CompletionLineEdit
from httprider.widgets.completion_plain_text import CompletionPlainTextEdit
from httprider.widgets.new_tag_entry_input import NewTagEntryLineEdit
from httprider.widgets.tag_label_widget import TagLabelWidget


class RequestPresenter:
    current: ApiCall

    def __init__(self, parent_view):
        self.current = None
        self.view = parent_view

        self.request_header_list_presenter = KeyValueListPresenter(
            self.view.lst_request_headers,
            self,
            key_completions=COMMON_HEADERS,
            value_completions=HTTP_CONTENT_TYPES,
        )
        self.request_param_list_presenter = KeyValueListPresenter(
            self.view.lst_request_params, self
        )
        self.form_params_list_presenter = KeyValueListPresenter(
            self.view.lst_form_params, self
        )

        self.mocked_response_presenter = MockedResponsePresenter(self, self.view)

        self.pyg_styles = styles_from_file(":/themes/pyg.css")
        self.view.txt_request_body.document().setDefaultStyleSheet(self.pyg_styles)

        self.assertion_builder_dialog = AssertionBuilderDialog(self.view)
        self.txt_new_tag_input = NewTagEntryLineEdit(self.view)
        self.view.tags_layout.addWidget(self.txt_new_tag_input)
        self.spacer_item = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )
        self.view.tags_layout.addItem(self.spacer_item)
        self.view.btn_send_request.pressed.connect(self.on_btn_send_request)
        self.view.btn_add_tag.pressed.connect(self.add_new_tag_label)
        self.txt_new_tag_input.save_tag_signal.connect(self.save_new_tag)
        self.txt_new_tag_input.discard_tag_signal.connect(self.discard_new_tag)
        self.view.btn_open_assertions_dialog.pressed.connect(
            self.on_show_assertions_dialog
        )

        app_settings.app_data_reader.signals.api_call_change_selection.connect(
            self.refresh
        )
        app_settings.app_data_writer.signals.api_call_tag_added.connect(self.refresh)
        app_settings.app_data_writer.signals.api_call_tag_removed.connect(self.refresh)
        app_settings.app_data_writer.signals.api_call_updated.connect(
            self.on_api_call_refresh
        )
        app_settings.app_data_writer.signals.api_test_case_changed.connect(
            self.refresh_completer
        )
        app_settings.app_data_writer.signals.environment_data_changed.connect(
            self.refresh_completer
        )
        app_settings.app_data_reader.signals.initial_cache_loading_completed.connect(
            self.refresh_completer
        )
        app_settings.app_data_writer.signals.exchange_added.connect(
            self.on_exchange_added
        )

        self.assertion_result_presenter = AssertionResultPresenter(self.view)

    def on_exchange_added(self, exchange):
        api_call_id = exchange.api_call_id
        api_test_case = app_settings.app_data_cache.get_api_test_case(api_call_id)
        self.assertion_result_presenter.evaluate(api_test_case, exchange)

    def refresh_completer(self):
        completer_model: QStandardItemModel = get_completer_model()
        self.view.txt_http_url.setup_completions(None, completer_model)
        self.view.txt_request_body.child_edit.setup_completer(completer_model)

    def on_show_data_generator_dialog(self):
        focused_widget: QWidget = qApp.focusWidget()
        if type(focused_widget) in [CompletionPlainTextEdit, CompletionLineEdit]:
            key_event = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_Dollar, Qt.NoModifier, "$")
            qApp.sendEvent(focused_widget, key_event)

    def on_show_assertions_dialog(self):
        self.assertion_builder_dialog.show_dialog(self.current)

    def get_api_description(self):
        return self.view.txt_api_description.toPlainText().strip()

    def form_to_object(self):
        url, qs = split_url_qs(self.view.txt_http_url.text().strip())
        self.current.http_method = self.get_http_method()
        self.current.http_url = url
        self.current.http_headers = self.get_headers()
        self.current.http_params = {**self.get_query_params(), **qs}
        self.current.form_params = self.get_form_params()
        self.current.http_request_body = self.get_request_body()
        self.current.title = self.view.txt_api_title.text().strip()
        self.current.description = self.get_api_description()
        self.current.tags = self.get_all_tags()
        self.current.mocked_response = self.get_mocked_response()

    def get_all_tags(self):
        all_tags = []
        for i in range(self.view.tags_layout.count()):
            widget_item = self.view.tags_layout.itemAt(i)
            if widget_item and (
                type(widget_item.widget()) is QLabel
                or type(widget_item.widget()) is TagLabelWidget
            ):
                all_tags.append(widget_item.widget().text().strip())

        return all_tags

    def get_mocked_response(self):
        return self.mocked_response_presenter.form_to_object()

    def object_to_form(self, api_call: ApiCall):
        self.current = api_call

        self.view.txt_http_url.setText(self.current.http_url)
        self.view.txt_api_title.setText(self.current.title)
        if self.get_api_description() != self.current.description:
            self.view.txt_api_description.setPlainText(self.current.description)
        index_to_set = self.view.cmb_http_method.findText(
            self.current.http_method.upper()
        )
        self.view.cmb_http_method.setCurrentIndex(index_to_set)
        self.update_headers_on_form(self.current.http_headers)
        self.update_query_params_on_form(self.current.http_params)
        self.update_form_params_on_form(self.current.form_params)
        if self.get_request_body() != self.current.http_request_body:
            self.view.txt_request_body.clear()
            self.view.txt_request_body.appendHtml(
                api_request_body_highlighted(self.current)
            )

        self.update_tags_on_form(self.current, self.current.tags)
        self.mocked_response_presenter.object_to_form(self.current.mocked_response)

        # Try setting the border to red
        # @todo: One way to indicate that JSON is invalid.
        # Not sure that best way to code it
        # self.view.txt_request_body.setStyleSheet("border: 1px solid red")
        # self.view.txt_request_body.setLineWidth(1)
        # self.view.txt_request_body.setObjectName("txt_api_description")

    def save_new_tag(self, new_tag):
        if new_tag not in self.current.tags:
            api_call_interactor.add_tag_to_api_call(self.current, new_tag)

        self.txt_new_tag_input.clear()
        self.txt_new_tag_input.hide()

    def display_new_tag_on_view(self, api_call, tag_name):
        tag_label_widget = TagLabelWidget(api_call, tag_name, self.view)
        tag_label_widget.remove_tag_signal.connect(self.remove_selected_tag)
        self.view.tags_layout.insertWidget(2, tag_label_widget)

    def remove_selected_tag(self, tag_name):
        api_call_interactor.remove_tag_from_api_call(self.current, tag_name)

    def discard_new_tag(self):
        self.txt_new_tag_input.clear()
        self.txt_new_tag_input.hide()

    def add_new_tag_label(self):
        self.txt_new_tag_input.show()
        self.txt_new_tag_input.setFocus()

    def remove_all_tags(self):
        i = 0
        while i < self.view.tags_layout.count():
            widget_item = self.view.tags_layout.itemAt(i)
            if widget_item and (
                type(widget_item.widget()) is QLabel
                or type(widget_item.widget()) is TagLabelWidget
            ):
                widget_in_item = widget_item.widget()
                widget_item.widget().hide()
                self.view.tags_layout.removeWidget(widget_in_item)
            else:
                i = i + 1

    def update_tags_on_form(self, api_call, api_call_tags):
        self.remove_all_tags()

        for tag in api_call_tags:
            self.display_new_tag_on_view(api_call, tag)

    def get_http_url(self):
        return self.view.txt_http_url.text()

    def get_http_method(self):
        cmb_current_index = self.view.cmb_http_method.currentIndex()
        return self.view.cmb_http_method.itemText(cmb_current_index)

    def get_headers(self):
        return self.request_header_list_presenter.get_items()

    def get_form_params(self):
        return self.form_params_list_presenter.get_items()

    def get_query_params(self):
        return self.request_param_list_presenter.get_items()

    def update_headers_on_form(self, headers):
        self.request_header_list_presenter.update_items(headers)

    def update_query_params_on_form(self, params):
        self.request_param_list_presenter.update_items(params)

    def update_form_params_on_form(self, params):
        self.form_params_list_presenter.update_items(params)

    def get_request_body(self):
        return self.view.txt_request_body.toPlainText().strip()

    def update_current_api_call(self):
        if not self.current:
            return

        self.form_to_object()
        api_call_interactor.update_api_call(self.current.id, self.current)

    def on_btn_send_request(self):
        self.update_current_api_call()
        rest_api_interactor.make_http_call(self.current)

    def on_api_call_refresh(self, _, api_call):
        self.refresh(api_call)

    def cleanup(self):
        """Called when all API calls are removed from list"""
        self.view.frame_request_response.hide()
        self.current = None

    def refresh(self, api_call: ApiCall):
        logging.info(f"Changed API Call to {api_call.id} => {api_call.title}")
        self.object_to_form(api_call)
