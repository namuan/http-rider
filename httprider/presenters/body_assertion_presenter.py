from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtWidgets import QTreeView, QAction, QMenu, qApp

from . import populate_tree_with_json
from httprider.widgets.json_tree_widget import ItemRole, JsonModel


class BodyAssertionPresenter:
    view: QTreeView

    def __init__(self, tbl_view, parent_view, on_body_selection):
        self.view = tbl_view
        self.parent_view = parent_view
        self.parent_body_selection = on_body_selection

        self.json_model = JsonModel()
        self.view.doubleClicked.connect(self.on_body_item_selected)

        # Pre-built context menus
        select_action = QAction("&Select Value", self.parent_view)
        select_action.triggered.connect(self.on_select_json)

        copy_action = QAction("&Copy Value to Clipboard", self.parent_view)
        copy_action.triggered.connect(self.on_body_item_clipboard_copy)

        self.context_menu = QMenu()
        self.context_menu.addAction(select_action)
        self.context_menu.addAction(copy_action)

        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.show_context_menu)

    def refresh(self, request_body):
        populate_tree_with_json(request_body or "{}", self.json_model, self.view)

    def on_select_json(self):
        selected_index = self.view.currentIndex()
        self.on_body_item_selected(selected_index)

    def show_context_menu(self, position):
        index: QModelIndex = self.view.indexAt(position)
        if not index.isValid():
            return
        self.context_menu.exec_(self.view.mapToGlobal(position))

    def on_body_item_selected(self, index: QModelIndex):
        item = self.view.model().data(index, ItemRole)
        if item.itemType is dict or item.itemType is list:
            return
        current_value = item.itemValue
        json_path = [item]
        while item.parent():
            json_path.append(item.parent())
            item = item.parent()
        json_path.reverse()
        self.parent_body_selection(json_path, current_value)

    def on_body_item_clipboard_copy(self):
        index = self.view.currentIndex()
        item = self.view.model().data(index, ItemRole)
        if item.itemType is dict or item.itemType is list:
            return
        current_value = item.itemValue

        clipboard = qApp.clipboard()
        clipboard.setText(current_value)
