import functools
import re

from PyQt6.QtWidgets import QTreeWidgetItem

from httprider.core import data_type
from httprider.core.constants import ASSERTION_TYPE_ROLE, AssertionDataSource
from httprider.core.core_settings import app_settings
from httprider.model.app_data import ApiCall, HttpExchange

from . import assertion_variable_name
from .assertion_list_presenter import AssertionListPresenter
from .body_assertion_presenter import BodyAssertionPresenter
from .headers_assertions_presenter import HeadersAssertionPresenter


class AssertionBuilderPresenter:
    current: ApiCall

    def __init__(self, parent_view):
        self.current = None
        self.current_api_test_case = None
        self.parent_view = parent_view
        self.parent_view.finished.connect(self.on_close)

        # Initialise Sub Presenters
        self.request_headers_presenter = HeadersAssertionPresenter(
            self.parent_view.tbl_request_headers,
            self.parent_view,
            self.on_request_header_selection,
        )
        self.response_headers_presenter = HeadersAssertionPresenter(
            self.parent_view.tbl_response_headers,
            self.parent_view,
            self.on_response_header_selection,
        )
        self.request_body_presenter = BodyAssertionPresenter(
            self.parent_view.tbl_request_body,
            self.parent_view,
            self.on_request_body_selected,
        )
        self.response_body_presenter = BodyAssertionPresenter(
            self.parent_view.tbl_response_body,
            self.parent_view,
            self.on_response_body_selected,
        )
        self.assertion_list_presenter = AssertionListPresenter(self, self.parent_view.tbl_assertions, self.parent_view)

    def json_path_builder(self, out, next_item):
        accum, parent_type = out
        if parent_type is list and next_item.itemKey.startswith("Index"):
            patterns = re.findall("Index.(\\d+)", next_item.itemKey)
            if patterns:
                return f"{accum}.[{patterns[0]}]", next_item.itemType

        if next_item.itemKey.startswith("Index"):
            patterns = re.findall("Index.(\\d+)", next_item.itemKey)
            if patterns:
                return f"{accum}.[{patterns[0]}]", next_item.itemType

        return f"{accum}.{next_item.itemKey}", next_item.itemType

    def on_request_body_selected(self, json_path, current_value):
        selector, _ = functools.reduce(self.json_path_builder, json_path[1:], ("$", dict))
        item = QTreeWidgetItem([
            AssertionDataSource.REQUEST_BODY.value,
            assertion_variable_name(self.current.title, AssertionDataSource.REQUEST_BODY.value, selector),
            selector,
            str(current_value),
        ])
        item.setData(3, ASSERTION_TYPE_ROLE, data_type(current_value))
        self.assertion_list_presenter.add_item(item, current_data=current_value)

    def on_response_body_selected(self, json_path, current_value):
        selector, _ = functools.reduce(self.json_path_builder, json_path[1:], ("$", dict))
        item = QTreeWidgetItem([
            AssertionDataSource.RESPONSE_BODY.value,
            assertion_variable_name(
                self.current.title,
                AssertionDataSource.RESPONSE_BODY.value,
                selector,
            ),
            selector,
            str(current_value),
        ])
        item.setData(3, ASSERTION_TYPE_ROLE, data_type(current_value))
        self.assertion_list_presenter.add_item(item, current_data=current_value)

    def on_request_header_selection(self, selected_item):
        item = QTreeWidgetItem([
            AssertionDataSource.REQUEST_HEADER.value,
            assertion_variable_name(
                self.current.title,
                AssertionDataSource.REQUEST_HEADER.value,
                selected_item.text(0),
            ),
            selected_item.text(0),
            selected_item.text(1),
        ])
        item.setData(3, ASSERTION_TYPE_ROLE, data_type(selected_item.text(1)))
        self.assertion_list_presenter.add_item(item, current_data=selected_item.text(1))

    def on_response_header_selection(self, selected_item):
        item = QTreeWidgetItem([
            AssertionDataSource.RESPONSE_HEADER.value,
            assertion_variable_name(
                self.current.title,
                AssertionDataSource.RESPONSE_HEADER.value,
                selected_item.text(0),
            ),
            selected_item.text(0),
            selected_item.text(1),
        ])
        item.setData(3, ASSERTION_TYPE_ROLE, data_type(selected_item.text(1)))
        self.assertion_list_presenter.add_item(item, current_data=selected_item.text(1))

    def load_configuration_dialog(self, api_call: ApiCall):
        self.current = api_call
        self.current_api_test_case = app_settings.app_data_cache.get_api_test_case(self.current.id)
        last_exchange: HttpExchange = app_settings.app_data_cache.get_last_exchange(api_call.id)

        self.request_headers_presenter.refresh(last_exchange.request.headers.items())
        self.response_headers_presenter.refresh(last_exchange.response.headers.items())
        self.request_body_presenter.refresh(last_exchange.request.request_body)
        self.response_body_presenter.refresh(last_exchange.response.response_body)
        self.assertion_list_presenter.refresh(self.current_api_test_case, last_exchange)

        self.parent_view.show()

    def on_close(self):
        self.current_api_test_case.assertions = self.assertion_list_presenter.get_all_assertions()
        app_settings.app_data_writer.upsert_assertions(self.current_api_test_case)
