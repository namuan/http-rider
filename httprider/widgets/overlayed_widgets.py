from PyQt6 import QtCore, QtWidgets


class FloatingButtonWidget(QtWidgets.QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.paddingLeft = 5
        self.paddingTop = 5

    def update_position(self):
        parent_rect = self.parent().viewport().rect() if hasattr(self.parent(), "viewport") else self.parent().rect()

        if not parent_rect:
            return

        x = parent_rect.width() - self.width() - self.paddingLeft
        y = self.paddingTop
        self.setGeometry(x, y, self.width(), self.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_position()

    def mousePressEvent(self, event):
        self.parent().floatingButtonClicked.emit()


class OverlayedPlainTextEdit(QtWidgets.QPlainTextEdit):
    floatingButtonClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.floating_button = FloatingButtonWidget(parent=self)

    def update_floating_button_text(self, txt):
        self.floating_button.setText(txt)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.floating_button.update_position()
