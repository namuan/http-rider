from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import QHeaderView, QMenu, QApplication
from PyQt6.QtGui import QAction
from . import populate_tree_with_kv_dict


class HeadersAssertionPresenter:
    def __init__(self, tbl_widget, parent_view, on_header_selection):
        self.view = tbl_widget
        self.parent_view = parent_view
        self.parent_header_selection = on_header_selection

        self.view.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.view.header().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        self.view.doubleClicked.connect(self.on_double_click_item)

        # Pre-built context menus
        select_action = QAction("&Select Value", self.parent_view)
        select_action.triggered.connect(self.on_select_header)

        copy_action = QAction("&Copy Value to Clipboard", self.parent_view)
        copy_action.triggered.connect(self.on_clipboard_copy_header)

        self.header_menu = QMenu()
        self.header_menu.addAction(select_action)
        self.header_menu.addAction(copy_action)

        self.view.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.view.customContextMenuRequested.connect(self.show_menu_headers)

    def on_double_click_item(self, index: QModelIndex):
        selected_item = self.view.itemFromIndex(index)
        self.parent_header_selection(selected_item)

    def on_clipboard_copy_header(self):
        selected_item = self.view.currentItem()
        clipboard = QApplication.instance().clipboard()
        clipboard.setText(selected_item.text(1))

    def on_select_header(self):
        selected_item = self.view.currentItem()
        self.parent_header_selection(selected_item)

    def show_menu_headers(self, position):
        index: QModelIndex = self.view.indexAt(position)
        if not index.isValid():
            return

        self.header_menu.exec(self.view.mapToGlobal(position))

    def refresh(self, header_items):
        populate_tree_with_kv_dict(header_items, self.view)
