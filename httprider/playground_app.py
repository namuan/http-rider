import sys
import traceback

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *

from .generated.playground import Ui_MainWindow
from .core.constants import *

API_CALL_ROLE = Qt.UserRole + 100
PADDING = 5


class PlaygroundWindow(QMainWindow, Ui_MainWindow):
    is_drop_operation: bool = False
    dropped_row: int = -1

    def __init__(self, parent=None):
        super(PlaygroundWindow, self).__init__(parent)
        self.counter = 0
        self.setupUi(self)

        model: QStandardItemModel = QStandardItemModel()
        for e in ["${API_URL}", "random", "data"]:
            item: QStandardItem = QStandardItem()
            item.setText(e)
            item.setData(e, DYNAMIC_STRING_ROLE)
            model.appendRow(item)

        self.lineEdit.setup_completions(None, model)

        sys.excepthook = PlaygroundWindow.log_uncaught_exceptions

    def clear_controls(self):
        self.model.clear()

    @staticmethod
    def log_uncaught_exceptions(cls, exc, tb) -> None:
        print(''.join(traceback.format_tb(tb)))
        print('{0}: {1}'.format(cls, exc))

    def setup_data(self):
        pass


def configure_theme(application):
    from .themes.light_theme import LightTheme
    application.setStyle(LightTheme())


if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = PlaygroundWindow()
    configure_theme(application)
    application.setStyleSheet("""
    """)
    window.setup_data()
    window.show()
    sys.exit(application.exec_())
