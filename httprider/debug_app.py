import sys

from PyQt5 import QtWidgets

from httprider.generated.debug_window import Ui_DebugWindow


class DebugWindow(QtWidgets.QMainWindow, Ui_DebugWindow):
    start: int = 0
    sel_length: int = 0

    def __init__(self, parent=None):
        super(DebugWindow, self).__init__(parent)
        self.setupUi(self)
        self.tabWidget.setStyleSheet("""
            border-top: 2px solid #C2C7CB;
            left: 15px; /* move to the right by 5px */

        """)
        # ui events

    def on_test(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = DebugWindow()
    window.show()
    sys.exit(app.exec_())
