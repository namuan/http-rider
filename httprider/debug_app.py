import sys

from PyQt5 import QtWidgets

from httprider.generated.debug_window import Ui_DebugWindow


class DebugWindow(QtWidgets.QMainWindow, Ui_DebugWindow):
    start: int = 0
    sel_length: int = 0

    def __init__(self, parent=None):
        super(DebugWindow, self).__init__(parent)
        self.setupUi(self)

        # ui events
        self.btn_test.clicked.connect(self.on_test)
        self.btn_select.clicked.connect(self.on_set_select)
        self.startVal.valueChanged.connect(self.on_update_select)
        self.endVal.valueChanged.connect(self.on_update_select)

    def on_test(self):
        whole_text = self.txt_val.text()
        selected_text = self.txt_val.selectedText()
        self.start = self.txt_val.selectionStart()
        self.sel_length = self.txt_val.selectionLength()

        output = f"W: {whole_text}, t: {selected_text}, s: {self.start}, l: {self.sel_length}"
        self.lbl_output.setText(output)

    def on_set_select(self):
        self.txt_val.setSelection(
            self.start,
            self.sel_length
        )

    def on_update_select(self):
        sv = self.startVal.value()
        ev = self.endVal.value()
        self.txt_val.setSelection(sv, ev)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = DebugWindow()
    window.show()
    sys.exit(app.exec_())
