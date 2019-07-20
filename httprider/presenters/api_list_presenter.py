import copy
import logging
from typing import List

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import *

from ..core.constants import *
from ..core.core_settings import app_settings
from ..core.rest_api_interactor import RestApiInteractor
from ..external.rest_api_connector import http_exchange_signals
from ..model.app_data import ApiCall, HttpExchange
from ..presenters import AssertionResultPresenter
from ..widgets.api_calls_list_view import ApiCallItemDelegate

PADDING = 5


class ApiListPresenter:
    model: QStandardItemModel
    view: QListView
    is_drop_operation: bool = False
    dropped_row: int = -1

    def __init__(self, parent_view):
        self.view = parent_view.lst_http_requests
        self.parent_view = parent_view
        self.interactor = RestApiInteractor()

        self.model = QStandardItemModel()
        self.view.setModel(self.model)
        self.view.setItemDelegate(ApiCallItemDelegate())

        self.view.selectionModel().currentChanged.connect(self.on_list_item_selected)
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.show_context_menu)
        self.view.drop_event_signal.connect(self.on_drop_event)
        self.view.model().rowsRemoved.connect(self.onRowsRemoved)

        http_exchange_signals.request_started.connect(self.on_request_started)

        # Context Menu setup
        duplicate_action = QAction("Duplicate", self.view)
        duplicate_action.triggered.connect(self._duplicate_request)

        remove_action = QAction("Delete", self.view)
        remove_action.triggered.connect(self.on_remove_selected_item)

        toggle_action = QAction("Toggle Enable/Disable", self.view)
        toggle_action.triggered.connect(self.on_toggle_request_status)

        self.menu = QMenu()
        self.menu.addAction(duplicate_action)
        self.menu.addAction(remove_action)
        self.menu.addAction(toggle_action)

        app_settings.app_data_writer.signals.api_call_added.connect(self.add_request_widget)
        app_settings.app_data_writer.signals.api_call_updated.connect(self.refresh_selected_item)
        app_settings.app_data_writer.signals.multiple_api_calls_added.connect(self.refresh_multiple_items)
        app_settings.app_data_writer.signals.selected_tag_changed.connect(self.refresh)

        self.assertion_result_presenter = AssertionResultPresenter(self.parent_view)

    def on_toggle_request_status(self):
        selected_model_index: QModelIndex = self.index_at_selected_row()
        if not selected_model_index:
            return
        api_call_id = selected_model_index.data(API_ID_ROLE)
        api_call: ApiCall = app_settings.app_data_reader.get_api_call(api_call_id)
        api_call.enabled = not api_call.enabled
        app_settings.app_data_writer.update_api_call(api_call_id, api_call)

    def on_drop_event(self, model_index: QModelIndex):
        self.is_drop_operation = True
        self.dropped_row = model_index.row()

    def show_context_menu(self, position):
        index: QModelIndex = self.view.indexAt(position)
        if not index.isValid():
            return

        self.menu.exec_(self.view.viewport().mapToGlobal(position))

    def selectPreviousApiCall(self):
        selected_index = self.index_at_selected_row()
        if not selected_index:
            return

        selected_row = selected_index.row()
        previous_row = selected_row - 1

        if previous_row >= 0:
            previous_item: QStandardItem = self.model.item(previous_row)
            self.view.setCurrentIndex(previous_item.index())

    def selectNextApiCall(self):
        selected_index = self.index_at_selected_row()
        if not selected_index:
            return

        selected_row = selected_index.row()
        next_row = selected_row + 1
        total_rows = self.model.rowCount()

        if next_row < total_rows:
            next_item: QStandardItem = self.model.item(next_row)
            self.view.setCurrentIndex(next_item.index())

    def onRowsRemoved(self):
        if self.is_drop_operation:
            self.is_drop_operation = False
            current_item = self.model.item(self.dropped_row)
            current_index = self.model.indexFromItem(current_item)

            api_call = current_item.data(API_CALL_ROLE)
            before = self.dropped_row - 1
            prev_sequence_number = 0
            if before >= 0:
                prev_api_call = self.model.item(before).data(API_CALL_ROLE)
                prev_sequence_number = prev_api_call.sequence_number
            total_rows = self.model.rowCount()
            after = self.dropped_row + 1
            if after >= total_rows:
                next_sequence_number = app_settings.app_data_writer.generate_sequence_number()
            else:
                next_api_call = self.model.item(after).data(API_CALL_ROLE)
                next_sequence_number = next_api_call.sequence_number
            new_sequence_number = prev_sequence_number + (next_sequence_number - prev_sequence_number) / 2
            api_call.sequence_number = new_sequence_number
            logging.info(f"API Call: {api_call.id} - "
                         f"New Sequence {new_sequence_number} - "
                         f"Moved between {prev_sequence_number} and {next_sequence_number}")
            app_settings.app_data_writer.update_api_call(api_call.id, api_call)
            self.view.setCurrentIndex(current_index)

    def add_request_widget(self, doc_id, api_call: ApiCall, select_item=True):
        logging.info(f"Adding new item with id {doc_id} to requests list - {api_call.title}")
        item = QStandardItem(api_call.title)
        item.setData(api_call, API_CALL_ROLE)
        item.setData(QVariant(api_call.id), API_ID_ROLE)
        item.setToolTip(api_call.description)
        item.setDragEnabled(True)
        item.setDropEnabled(False)
        self.model.appendRow(item)
        if select_item:
            index = self.model.indexFromItem(item)
            self.view.setCurrentIndex(index)

    def run_all_api_calls(self):
        total_rows = self.model.rowCount()
        logging.debug("** Running multiple API calls: {}".format(total_rows))
        for n in range(total_rows):
            api_call = self.model.item(n).data(API_CALL_ROLE)
            logging.debug("** Multiple APIs: API Call {}".format(api_call.id))
            if api_call.enabled:
                self.interactor.make_http_call(api_call, on_success=self.on_success)

    def on_success(self, exchange: HttpExchange):
        api_test_case = app_settings.app_data_reader.get_api_test_case(exchange.api_call_id)
        self.assertion_result_presenter.evaluate(api_test_case, exchange)

    def on_remove_selected_item(self):
        selected_model_index: QModelIndex = self.index_at_selected_row()
        if not selected_model_index:
            return
        row_to_remove = selected_model_index.row()
        api_call: ApiCall = selected_model_index.data(API_CALL_ROLE)
        app_settings.app_data_writer.remove_api_call([api_call.id])
        previous_row = row_to_remove - 1
        if previous_row >= 0:
            previous_item: QStandardItem = self.model.item(previous_row)
            self.view.setCurrentIndex(previous_item.index())

    def on_list_item_selected(self, current: QModelIndex):
        if not current:
            return

        selected_api_call: ApiCall = current.data(API_CALL_ROLE)
        app_settings.app_data_reader.update_selected_api_call(selected_api_call.id)

    def on_request_started(self, _, api_call_id):
        api_call_row = self.__row_for_api_call(api_call_id)
        item_running = self.model.item(api_call_row)
        index_running = self.model.indexFromItem(item_running)
        self.view.setCurrentIndex(index_running)

    def refresh_selected_item(self, api_call_id):
        api_call_row = self.__row_for_api_call(api_call_id)
        if api_call_row != -1:
            api_call = app_settings.app_data_reader.get_api_call(api_call_id)
            self.model.item(api_call_row).setData(api_call, API_CALL_ROLE)

    def refresh_multiple_items(self, doc_ids: List[str], api_calls: List[ApiCall]):
        assert len(doc_ids) == len(api_calls)
        for doc_id, api_call in zip(doc_ids, api_calls):
            self.add_request_widget(doc_id, api_call, select_item=False)

    def on_search_query(self, search_query):
        app_settings.app_data_cache.update_search_query(search_query)
        self.refresh()

    def refresh(self):
        """Re-renders this list view and selects the first item"""
        self.model.clear()
        app_state = app_settings.app_data_cache.get_app_state()
        api_calls = app_settings.app_data_cache.filter_api_calls(
            search_query=app_state.selected_search,
            search_tag=app_state.selected_tag
        )
        for api in api_calls:
            self.add_request_widget(api.id, api, select_item=False)

        if len(api_calls) > 0:
            first_item: QStandardItem = self.model.item(0)
            self.view.setCurrentIndex(first_item.index())

    def index_at_selected_row(self):
        selected_model: QItemSelectionModel = self.view.selectionModel()
        if not selected_model.hasSelection():
            return None
        return selected_model.currentIndex()

    def _duplicate_request(self):
        selected_index = self.index_at_selected_row()
        if not selected_index:
            return
        api_call = selected_index.data(API_CALL_ROLE)
        duplicate_api_call = copy.deepcopy(api_call)
        duplicate_api_call.title = f"{duplicate_api_call.title} Duplicate"
        duplicate_api_call.last_response_code = 0
        duplicate_api_call.sequence_number = app_settings.app_data_writer.generate_sequence_number()
        app_settings.app_data_writer.add_api_call(duplicate_api_call)

    def __row_for_api_call(self, api_call_id):
        api_call_row = next(
            (n for n in range(self.model.rowCount()) if self.model.item(n).data(API_ID_ROLE) == api_call_id),
            -1
        )
        return api_call_row
