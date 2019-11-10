from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QKeyEvent, QFocusEvent


# noinspection PyPep8Naming
class NewTagEntryLineEdit(QtWidgets.QLineEdit):
    save_tag_signal = QtCore.pyqtSignal(str)
    discard_tag_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(NewTagEntryLineEdit, self).__init__(parent)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setClearButtonEnabled(True)
        self.hide()

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        if event.key() == QtCore.Qt.Key_Escape:
            self.discard_tag_signal.emit()

        if event.key() in [QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            self.save_tag_signal.emit(self.text())

    def focusOutEvent(self, event: QFocusEvent):
        if self.text():
            self.save_tag_signal.emit(self.text())
        else:
            self.discard_tag_signal.emit()

        super().focusOutEvent(event)
