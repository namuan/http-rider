from PyQt5.QtCore import *
from PyQt5.QtGui import QKeyEvent, QFocusEvent, QStandardItemModel, QCursor
from PyQt5.QtWidgets import *

from ..core.constants import DYNAMIC_STRING_ROLE
from ..core.generators import file_func_generator
from ..ui import open_file
from ..ui.data_generator_dialog import DataGeneratorDialog


class ChildLineEdit(QLineEdit):
    some_signal = pyqtSignal(str, str, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrame(False)
        self.setStyleSheet("""
        background-color: #2882af;
        color: white;
        border-style: none;
        border-radius: 2px;        
        """)
        self.hide()

    def setup_completer(self, model: QStandardItemModel):
        completer = QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        super().setCompleter(completer)
        self.completer().activated[QModelIndex].connect(self.on_completion)

    def on_completion(self, index: QModelIndex):
        self.some_signal.emit(index.data(Qt.DisplayRole), index.data(DYNAMIC_STRING_ROLE), False)

    def focusOutEvent(self, e: QFocusEvent):
        if self.completer().popup().isVisible():
            self.some_signal.emit("", "", True)

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Escape:
            self.some_signal.emit("", "", True)
            e.ignore()

        super().keyPressEvent(e)


class CompletionLineEdit(QLineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_generator_dialog = DataGeneratorDialog(self)
        self.child_edit = ChildLineEdit(self)
        self.child_edit.some_signal.connect(self.pre_completion_check)
        self._selected_text = None
        self._selection_start = 0
        self._selection_end = 0

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
        elif display_text == "file":
            file_location, _ = open_file(self, "Select File")
            file_function = file_func_generator(file_location, wrap_in_quotes=True)
            self.process_completion(file_function, file_function, rollback)
        else:
            self.process_completion(display_text, variable_name, rollback)

    def process_completion(self, display_text, variable_name, rollback=False):
        self.child_edit.completer().popup().hide()
        self.child_edit.hide()
        self.child_edit.setText("")

        self.setFocus(Qt.OtherFocusReason)
        if not rollback:
            if self._selected_text:
                self.setSelection(self._selection_start, self._selection_end)

            self.insert(variable_name)

    def setup_completions(self, parent_completer, child_completer_model):
        if parent_completer:
            super().setCompleter(parent_completer)

        if child_completer_model:
            self.child_edit.setup_completer(child_completer_model)

    def keyPressEvent(self, e: QKeyEvent):
        if not self.child_edit.completer():
            super().keyPressEvent(e)
            return

        popup_visible = self.child_edit.completer().popup().isVisible()

        if e.key() == Qt.Key_Dollar:
            if not popup_visible:
                self._selected_text = self.selectedText()
                self._selection_start = self.selectionStart()
                self._selection_end = self.selectionEnd()
                self.child_edit.setGeometry(self.rect())
                self.child_edit.setText("")
                self.child_edit.show()
                self.child_edit.setFocus(Qt.OtherFocusReason)
                return

        super().keyPressEvent(e)
