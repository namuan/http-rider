from PyQt5.QtCore import *

from ..core import load_json_show_error

NoneType = type(None)
ItemRole = Qt.UserRole + 200


class JsonTreeItem(object):
    def __init__(self, parent=None):
        self.parentItem = parent
        self.childItems = []
        self.itemKey = None
        self.itemValue = None
        self.itemType = None

    def appendChild(self, childItem):
        self.childItems.append(childItem)

    def child(self, row: int):
        return self.childItems[row]

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem is not None:
            return self.parentItem.childItems.index(self)
        return 0

    def childCount(self):
        return len(self.childItems)

    def load_json(self, json_data, key="$", parent=None):
        topItem = JsonTreeItem(parent)
        topItem.itemKey = key
        topItem.itemType = json_data.__class__

        if isinstance(json_data, dict):
            for k, v in json_data.items():
                child = self.load_json(v, k, topItem)
                topItem.appendChild(child)
        elif isinstance(json_data, list):
            for index, item in enumerate(json_data):
                child = self.load_json(item, f"Index {index}", topItem)
                topItem.appendChild(child)
        else:
            topItem.itemValue = self.__flatten_string(json_data) if isinstance(json_data, str) else json_data
            topItem.itemValue = self.__flatten_string(json_data) if isinstance(json_data, str) else json_data

        return topItem

    def __flatten_string(self, input):
        return input.strip().replace('\r', '').replace('\n', '')


class JsonModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.headerItems = ["Key", "Value"]
        self.rootItem = JsonTreeItem()

    def setup_model(self, json_str):
        self.clear()
        json_data = load_json_show_error(json_str)
        self.beginResetModel()
        nestedRoot = self.rootItem.load_json(json_data)
        self.rootItem.appendChild(nestedRoot)
        self.endResetModel()

    def data(self, index: QModelIndex, role=None):
        if not index.isValid():
            return QVariant()

        item = index.internalPointer()
        col = index.column()

        if role == Qt.DisplayRole:
            if col == 0:
                return item.itemKey
            elif col == 1:
                return item.itemValue

        if role == ItemRole:
            return item

        return QVariant()

    def __convert_to_json_type(self, clazz):
        if clazz is str:
            return "String"
        elif clazz is dict:
            return "Object"
        elif clazz is list:
            return "Array"
        elif clazz is int or clazz is float:
            return "Number"
        elif clazz is bool:
            return "Boolean"
        elif clazz is NoneType:
            return "Null"
        else:
            return str(clazz)

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headerItems[section]

        return None

    def parent(self, index: QModelIndex = None):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem or parentItem is None:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def columnCount(self, parent=None, *args, **kwargs):
        return 2

    def index(self, row, column, parent=QModelIndex, *args, **kwargs):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        return self.createIndex(row, column, childItem)

    def clear(self):
        self.rootItem = JsonTreeItem()
