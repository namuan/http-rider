from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import *

from httprider.core import DynamicStringData
from httprider.core.core_settings import app_settings
from httprider.model.completer import get_completer_model
from httprider.widgets.key_value_widget import KeyValueWidget
from httprider.widgets.new_header_widget import NewItemButtonWidget


class KeyValueListPresenter:
    def __init__(self, lst_view, parent=None, key_completions=None, value_completions=None):
        self.lst_view = lst_view
        self.parent_view = parent
        self._completer = None
        self.add_new_item_widget()

        app_settings.app_data_writer.signals.api_test_case_changed.connect(self.refresh_completer)
        app_settings.app_data_writer.signals.environment_data_changed.connect(self.refresh_completer)
        app_settings.app_data_reader.signals.initial_cache_loading_completed.connect(self.refresh_completer)

        self.header_name_completer = None
        if key_completions:
            self.header_name_completer = QCompleter(key_completions)
            self.header_name_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.header_name_completer.setFilterMode(Qt.MatchFlag.MatchContains)
            self.header_name_completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        self.header_value_completer = None
        if value_completions:
            self.header_value_completer = QCompleter(value_completions)
            self.header_value_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.header_value_completer.setFilterMode(Qt.MatchFlag.MatchContains)
            self.header_value_completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        self.completer_model = None

    def refresh_completer(self):
        completer_model: QStandardItemModel = get_completer_model()
        self.completer_model = completer_model
        for i in range(self.lst_view.count() - 1):
            item = self.lst_view.item(i)
            widget = self.lst_view.itemWidget(item)
            widget.txt_value.setup_completions(self.header_value_completer, self.completer_model)

    def add_widget(self, header_name, header_value, item_position):
        item = QListWidgetItem()
        kv_widget = KeyValueWidget(self.lst_view, item, self.remove_item)
        kv_widget.txt_name.setCompleter(self.header_name_completer)
        kv_widget.txt_value.setup_completions(self.header_value_completer, self.completer_model)
        kv_widget.set_data(header_name, header_value)
        item.setSizeHint(kv_widget.sizeHint())
        self.lst_view.insertItem(item_position, item)
        self.lst_view.setItemWidget(item, kv_widget)

    def add_new_item_widget(self):
        item = QListWidgetItem()
        new_item_widget = NewItemButtonWidget(self.lst_view, item, self.add_new_item)
        item.setSizeHint(new_item_widget.sizeHint())

        self.lst_view.addItem(item)
        self.lst_view.setItemWidget(item, new_item_widget)

    def remove_item(self, widget_item):
        self.lst_view.takeItem(self.lst_view.row(widget_item))

    def add_new_item(self):
        total_items = self.lst_view.count()
        self.add_widget("", DynamicStringData(), total_items - 1)

    def get_items(self):
        kv_items = {}
        for i in range(self.lst_view.count() - 1):
            item = self.lst_view.item(i)
            widget = self.lst_view.itemWidget(item)
            k, v = widget.get_data()
            kv_items[k] = v
        return kv_items

    def update_items(self, items):
        self.lst_view.clear()
        for i, (k, v) in enumerate(items.items()):
            self.add_widget(k, v, i)

        self.add_new_item_widget()

    def clear(self):
        self.lst_view.clear()
        self.add_new_item_widget()
