from PyQt6 import QtWidgets

from ..core import DynamicStringData
from ..generated.key_value_widget import Ui_KeyValueWidget


class KeyValueWidget(QtWidgets.QWidget, Ui_KeyValueWidget):
    def __init__(self, parent=None, parent_widget_item=None, on_remove_callback=None):
        super(KeyValueWidget, self).__init__(parent)
        self.setupUi(self)
        self.k = ""
        self.v = DynamicStringData()
        self.setLayout(self.horizontalLayout)
        self.btn_remove_header.pressed.connect(
            lambda: on_remove_callback(parent_widget_item)
        )

    def set_data(self, name, v: DynamicStringData):
        self.k = name
        self.v = v

        self.txt_name.setText(self.k)
        self.txt_value.setValue(self.v)
        self.chk_field_enabled.setChecked(v.is_enabled)

    def get_data(self):
        self.k = self.txt_name.text().strip()
        self.v = self.txt_value.getValue()
        self.v.is_enabled = self.chk_field_enabled.isChecked()
        return self.k, self.v
