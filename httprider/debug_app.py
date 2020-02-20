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

    def on_test(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = DebugWindow()
    window.show()
    sys.exit(app.exec_())
