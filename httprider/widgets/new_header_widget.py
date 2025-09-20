from PyQt6 import QtWidgets

from httprider.generated.new_item_widget import Ui_NewItemWidget


class NewItemButtonWidget(QtWidgets.QWidget, Ui_NewItemWidget):
    def __init__(self, parent=None, parent_widget_item=None, on_add_new_header_pressed=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setLayout(self.horizontalLayout)
        self.parent_widget_item = parent_widget_item
        self.btn_new_header.pressed.connect(on_add_new_header_pressed)
