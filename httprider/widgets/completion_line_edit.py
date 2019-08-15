from PyQt5.QtCore import *
from PyQt5.QtGui import QKeyEvent, QFocusEvent, QStandardItemModel
from PyQt5.QtWidgets import *

from ..core import str_to_base64, DynamicStringData, DynamicStringType
from ..core.constants import DYNAMIC_STRING_ROLE
from ..core.generators import file_func_generator
from ..ui import open_file
from ..ui.data_generator_dialog import DataGeneratorDialog
from ..ui.utility_functions_dialog import UtilityFunctionsDialog


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
        self.some_signal.emit(
            index.data(Qt.DisplayRole),
            index.data(DYNAMIC_STRING_ROLE),
            False
        )

    def focusOutEvent(self, e: QFocusEvent):
        if self.completer().popup().isVisible():
            self.some_signal.emit("", "", True)

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Escape:
            self.some_signal.emit("", "", True)
            e.ignore()

        super().keyPressEvent(e)


class CompletionContextMenu(QMenu):
    def __init__(self, view):
        super().__init__(view)
        self.view = view
        # Context Menu setup
        b64_encode = QAction("Base64 Encode", self.view)
        b64_encode.triggered.connect(self.on_base_64_encode)

        enable_secret = QAction("Secret Hide/Show", self.view)
        enable_secret.triggered.connect(self.on_secret_value)

        self.addAction(b64_encode)
        self.addAction(enable_secret)

    def on_secret_value(self):
        dynamic_value: DynamicStringData = self.view.getValue()

        # Switch from secret -> plain, plain -> secret
        if self.view.echoMode() == QLineEdit.PasswordEchoOnEdit:
            dynamic_value.string_type = DynamicStringType.PLAIN.value
        else:
            dynamic_value.string_type = DynamicStringType.SECRET.value

        self.view.setValue(dynamic_value)

    def on_base_64_encode(self):
        whole_text = self.view.text()
        selected_fragment = self.view.selectedText()
        new_val = str_to_base64(selected_fragment or whole_text)
        if selected_fragment:
            self.view.insert(new_val)
        else:
            self.view.selectAll()
            self.view.insert(new_val)


class CompletionLineEdit(QLineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_generator_dialog = DataGeneratorDialog(self)
        self.utility_functions_dialog = UtilityFunctionsDialog(self)
        self.child_edit = ChildLineEdit(self)
        self.child_edit.some_signal.connect(self.pre_completion_check)
        self.selected_text = None
        self.selection_start = 0
        self.selection_length = 0

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        # @todo: Use createStandardContextMenu to extend the existing menu
        self.menu = CompletionContextMenu(self)

    def on_context_menu(self, position):
        self.menu.exec_(self.mapToGlobal(position))

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
        elif display_text == "tools":
            r: QRect = self.child_edit.rect()
            p = self.mapToGlobal(QPoint(r.x(), r.y() + r.height()))
            self.utility_functions_dialog.move(p)
            if self.utility_functions_dialog.exec_dialog() == QDialog.Accepted:
                f = self.utility_functions_dialog.get_function()
                self.process_completion(f, f, rollback, replace_text=True)
            else:
                self.process_completion(None, None, rollback=True)
        elif display_text == "file":
            file_location, _ = open_file(self, "Select File")
            file_function = file_func_generator(file_location, wrap_in_quotes=True)
            self.process_completion(file_function, file_function, rollback)
        else:
            self.process_completion(display_text, variable_name, rollback)

    def process_completion(self, display_text, variable_name, rollback=False, replace_text=False):
        self.child_edit.completer().popup().hide()
        self.child_edit.hide()
        self.child_edit.setText("")

        self.setFocus(Qt.OtherFocusReason)
        if not rollback:
            if replace_text:
                self.selectAll()

            if self.selected_text:
                self.setSelection(self.selection_start, self.selection_length)

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
                self.selected_text = self.selectedText()
                self.selection_start = self.selectionStart()
                self.selection_length = self.selectionLength()
                self.child_edit.setGeometry(self.rect())
                self.child_edit.setText("")
                self.child_edit.show()
                self.child_edit.setFocus(Qt.OtherFocusReason)
                return

        super().keyPressEvent(e)

    def setValue(self, new_val: DynamicStringData):
        if new_val.string_type == DynamicStringType.SECRET.value:
            self.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        else:
            self.setEchoMode(QLineEdit.Normal)

        self.setText(new_val.display_text)

    def getValue(self):
        field_val = self.text().strip()
        display_text = self.text().strip()
        string_type = DynamicStringType.PLAIN.value
        if self.echoMode() == QLineEdit.PasswordEchoOnEdit:
            string_type = DynamicStringType.SECRET.value

        return DynamicStringData(
            display_text=display_text,
            value=field_val,
            string_type=string_type
        )
