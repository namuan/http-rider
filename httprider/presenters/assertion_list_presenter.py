import logging
from functools import partial

from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QTreeWidgetItem, QHeaderView, QStyledItemDelegate, QComboBox, QTreeWidget, QPushButton

from ..core import elapsed_time_formatter, response_code_formatter
from ..core.constants import ASSERTION_TYPE_ROLE, AssertionMatchers
from ..core.core_settings import app_settings
from ..model.app_data import Assertion, AssertionDataSource, HttpExchange
from . import string_to_variable_name


class NoEditDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, widget, style, index):
        return None


class AssertionListPresenter:
    view: QTreeWidget

    def __init__(self, parent_presenter, tbl_widget, parent_view):
        self.parent_presenter = parent_presenter
        self.view = tbl_widget
        self.parent_view = parent_view
        stretch_mode = QHeaderView.Stretch
        header: QHeaderView = self.view.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, stretch_mode)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, stretch_mode)
        header.setSectionResizeMode(6, QHeaderView.Fixed)
        header.resizeSection(6, 40)
        self.view.setItemDelegateForColumn(0, NoEditDelegate(self.view))
        self.view.setItemDelegateForColumn(3, NoEditDelegate(self.view))

        self.parent_view.btn_response_code_assertion.pressed.connect(self.add_response_code_assertion)
        self.parent_view.btn_response_time_assertion.pressed.connect(self.add_response_time_assertion)

    def add_response_code_assertion(self):
        api_call = self.parent_presenter.current
        last_exchange: HttpExchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        current_response_code = response_code_formatter(last_exchange.response.http_status_code)
        item = QTreeWidgetItem([
            AssertionDataSource.RESPONSE_CODE.value,
            string_to_variable_name(api_call.title, AssertionDataSource.RESPONSE_CODE.value, ""),
            None,
            current_response_code
        ])
        item.setData(3, ASSERTION_TYPE_ROLE, 'int')
        self.add_item(item, current_data=current_response_code)

    def add_response_time_assertion(self):
        api_call = self.parent_presenter.current
        last_exchange: HttpExchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        current_elapsed_time = elapsed_time_formatter(last_exchange.response.elapsed_time)
        item = QTreeWidgetItem([
            AssertionDataSource.RESPONSE_TIME.value,
            string_to_variable_name(api_call.title, AssertionDataSource.RESPONSE_TIME.value, ""),
            None,
            current_elapsed_time
        ])
        item.setData(3, ASSERTION_TYPE_ROLE, 'float')
        self.add_item(item, current_data=current_elapsed_time)

    def add_item(self, item: QTreeWidgetItem, selected_matcher=None, current_data=None):
        existing_item = self.__assertion_exist(item)

        if not existing_item:
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.view.addTopLevelItem(item)
            item_qombo = QComboBox(self.view)
            item_qombo.addItems([e.value for e in AssertionMatchers])
            if selected_matcher:
                item_qombo.setCurrentText(selected_matcher)
            else:
                item_qombo.setCurrentText("---")

            self.view.setItemWidget(item, 4, item_qombo)
            delete_btn = QPushButton("X")
            delete_btn.setFlat(True)
            delete_btn.pressed.connect(partial(self.on_delete_assertion, item))
            self.view.setItemWidget(item, 6, delete_btn)
        else:
            existing_item.setData(3, Qt.DisplayRole, current_data)

    def on_delete_assertion(self, item: QTreeWidgetItem):
        index: QModelIndex = self.view.indexFromItem(item)
        self.view.takeTopLevelItem(index.row())

    def get_all_assertions(self):
        tests = []
        for i in range(self.view.topLevelItemCount()):
            widget_item: QTreeWidgetItem = self.view.topLevelItem(i)
            data_from = widget_item.data(0, Qt.DisplayRole)
            var_name = widget_item.data(1, Qt.DisplayRole)
            selector = widget_item.data(2, Qt.DisplayRole)
            assertion_value_type = widget_item.data(3, ASSERTION_TYPE_ROLE)
            selected_matcher = self.__selected_matcher(widget_item)
            expected_value = widget_item.data(5, Qt.DisplayRole)

            if selected_matcher == AssertionMatchers.NOT_NULL.value:
                expected_value = "Not Null"

            new_assertion = Assertion(
                data_from=data_from,
                var_name=var_name,
                selector=selector,
                matcher=selected_matcher,
                expected_value=expected_value,
                var_type=assertion_value_type
            )

            tests.append(new_assertion)

        return tests

    def __assertion_exist(self, item: QTreeWidgetItem):
        data_from = item.data(0, Qt.DisplayRole)
        selector = item.data(2, Qt.DisplayRole)
        assertion_found = None
        for i in range(self.view.topLevelItemCount()):
            widget_item: QTreeWidgetItem = self.view.topLevelItem(i)
            if widget_item.data(0, Qt.DisplayRole) == data_from and widget_item.data(2, Qt.DisplayRole) == selector:
                assertion_found = widget_item
                break
        return assertion_found

    def __selected_matcher(self, widget_item: QTreeWidgetItem):
        qombo: QComboBox = self.view.itemWidget(widget_item, 4)
        return qombo.currentText()

    def refresh(self, api_test_case, last_exchange: HttpExchange):
        self.parent_view.tbl_assertions.clear()
        formatted_response_code = response_code_formatter(last_exchange.response.http_status_code)
        self.parent_view.btn_response_code_assertion.setText(f"HTTP {formatted_response_code}")
        elapsed_time = elapsed_time_formatter(last_exchange.response.elapsed_time)
        self.parent_view.btn_response_time_assertion.setText(elapsed_time)

        for assertion in api_test_case.assertions:
            item = QTreeWidgetItem()

            current_value_from_exchange = "Unable to retrieve value"

            try:
                current_value_from_exchange = \
                    app_settings.app_data_cache.get_latest_assertion_value_from_exchange(assertion, last_exchange)
            except Exception as e:
                logging.error("Unable to retrieve value")
                logging.error(assertion)
                logging.error(last_exchange)

            # @todo: Create a function to convert row in assertions table <-> Assertion object
            item.setData(0, Qt.DisplayRole, assertion.data_from)
            item.setData(1, Qt.DisplayRole, assertion.var_name)
            item.setData(2, Qt.DisplayRole, assertion.selector)
            item.setData(3, Qt.DisplayRole, current_value_from_exchange)
            item.setData(3, ASSERTION_TYPE_ROLE, assertion.var_type)
            item.setData(5, Qt.DisplayRole, assertion.expected_value)
            self.add_item(
                item,
                selected_matcher=assertion.matcher,
                current_data=current_value_from_exchange
            )
