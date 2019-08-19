from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QTextCursor, QKeyEvent, QTextCharFormat
from PyQt5.QtWidgets import QPlainTextEdit, QDialog

from ..ui.data_generator_dialog import DataGeneratorDialog
from ..widgets.completion_line_edit import ChildLineEdit, QPoint


class CompletionPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_generator_dialog = DataGeneratorDialog(self)
        self.child_edit = ChildLineEdit(self)
        self.child_edit.entry_completed.connect(self.pre_completion_check)
        self.selected_text = None
        self.selection_start = 0
        self.selection_end = 0

    def pre_completion_check(self, display_text, variable_name, rollback=False):
        """Checks if one of the keyword is entered
        So that it can display appropriate dialog box
        Otherwise pass it to process completion
        """
        if display_text == "data":
            r: QRect = self.child_edit.rect()
            p = self.mapToGlobal(QPoint(r.x(), r.y() + r.height()))
            self.data_generator_dialog.move(p)
            if self.data_generator_dialog.exec_dialog() == QDialog.Accepted:
                f = self.data_generator_dialog.get_function()
                self.process_completion(f, f, rollback)
            else:
                self.process_completion(None, None, rollback=True)
        else:
            self.process_completion(display_text, variable_name, rollback)

    def process_completion(self, display_text, variable_name, rollback=False):
        self.child_edit.completer().popup().hide()
        self.child_edit.hide()
        self.child_edit.setText("")

        self.setFocus(Qt.OtherFocusReason)
        if not rollback:
            if self.selected_text:
                tc: QTextCursor = self.textCursor()
                tc.setPosition(self.selection_start)
                tc.setPosition(self._selection_end, QTextCursor.KeepAnchor)
                self.setTextCursor(tc)

            existing_format = self.currentCharFormat()
            tf: QTextCharFormat = QTextCharFormat()
            tf.setToolTip(display_text)
            self.setCurrentCharFormat(tf)
            self.insertPlainText(variable_name)
            self.setCurrentCharFormat(existing_format)

    def boundingRect(self):
        cr: QRect = self.cursorRect()
        pr: QRect = self.rect()
        cp = cr.x() - pr.x()
        bw = pr.width() - cp - 10
        cr.setWidth(bw)
        return cr

    def keyPressEvent(self, e: QKeyEvent):
        if not self.child_edit.completer():
            super().keyPressEvent(e)
            return

        popup_visible = self.child_edit.completer().popup().isVisible()
        if e.key() == Qt.Key_Dollar:
            if not popup_visible:
                tc: QTextCursor = self.textCursor()
                self.selected_text = tc.selectedText()
                self.selection_start = tc.selectionStart()
                self._selection_end = tc.selectionEnd()
                tc.setPosition(tc.selectionStart())
                self.setTextCursor(tc)
                popup_rect = self.boundingRect()
                self.child_edit.setGeometry(popup_rect)
                self.child_edit.setText("")
                self.child_edit.show()
                self.child_edit.setFocus(Qt.OtherFocusReason)
                return

        super().keyPressEvent(e)
