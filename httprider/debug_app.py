import sys

from PyQt5 import QtWidgets

from httprider.generated.debug_window import Ui_DebugWindow


class DebugWindow(QtWidgets.QMainWindow, Ui_DebugWindow):
    start: int = 0
    sel_length: int = 0
    edit_mode = True

    def __init__(self, parent=None):
        super(DebugWindow, self).__init__(parent)
        self.setupUi(self)
        # ui events
        self.plainTextEdit.floatingButtonClicked.connect(self.on_test)
        self.update_floating_button_text()

    def on_test(self):
        self.edit_mode = not self.edit_mode
        self.plainTextEdit.appendPlainText("Button Clicked - Mode: {}".format("Edit" if self.edit_mode else "Preview"))
        self.update_floating_button_text()

    def update_floating_button_text(self):
        if self.edit_mode:
            self.plainTextEdit.update_floating_button_text("Edit")
        else:
            self.plainTextEdit.update_floating_button_text("Preview")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = DebugWindow()
    window.show()
    sys.exit(app.exec_())
