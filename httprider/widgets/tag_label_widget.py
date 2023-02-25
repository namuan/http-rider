from PyQt6 import QtCore, QtGui, QtWidgets

from httprider.core.api_call_interactor import api_call_interactor
from ..core.core_settings import app_settings
from ..generated.tag_label_widget import Ui_TagLabelWidget
from ..model.app_data import ApiCall
from ..widgets.new_tag_entry_input import NewTagEntryLineEdit


class TagLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(TagLabel, self).__init__(parent)
        self.setStyleSheet("padding-left:1")
        self.setLineWidth(0)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class TagLabelWidget(QtWidgets.QWidget, Ui_TagLabelWidget):
    remove_tag_signal = QtCore.pyqtSignal(str)
    api_call: ApiCall = None
    old_tag = None

    def __init__(self, api_call: ApiCall, tag_name, parent=None):
        super(TagLabelWidget, self).__init__(parent)
        self.setupUi(self)
        self.lbl_tag = TagLabel(self.horizontalLayoutWidget)
        self.lbl_tag.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))
        self.lbl_tag.clicked.connect(self.editTag)
        self.horizontalLayout.insertWidget(0, self.lbl_tag)
        self.edit_tag = NewTagEntryLineEdit(self.horizontalLayoutWidget)
        self.edit_tag.save_tag_signal.connect(self.save_changed_tag)
        self.edit_tag.discard_tag_signal.connect(self.discard_changed_tag)
        self.horizontalLayout.insertWidget(0, self.edit_tag)
        self.setLayout(self.horizontalLayout)
        self.btn_tag_remove.pressed.connect(self.removeTag)
        self.__update_data(api_call, tag_name)

    def removeTag(self):
        self.remove_tag_signal.emit(self.lbl_tag.text())

    def text(self):
        return self.lbl_tag.text()

    def editTag(self):
        self.old_tag = self.text()
        self.edit_tag.setText(self.text())
        self.edit_tag.setSelection(0, len(self.edit_tag.text()))
        self.__in_edit_mode()

    def save_changed_tag(self, new_tag):
        self.__in_view_mode()
        self.__update_data(self.api_call, new_tag)

        api_call_interactor.rename_tag_in_api_call(self.api_call, self.old_tag, new_tag)

    def discard_changed_tag(self):
        self.__in_view_mode()

    def __in_view_mode(self):
        self.edit_tag.clear()
        self.edit_tag.hide()
        self.lbl_tag.show()
        self.btn_tag_remove.show()

    def __in_edit_mode(self):
        self.edit_tag.show()
        self.edit_tag.setFocus()
        self.lbl_tag.hide()
        self.btn_tag_remove.hide()

    def __update_data(self, api_call, tag_name):
        self.api_call = api_call
        self.lbl_tag.setText(tag_name)
