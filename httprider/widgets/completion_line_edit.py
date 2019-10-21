from PyQt5.QtCore import *
from PyQt5.QtGui import QKeyEvent, QFocusEvent, QStandardItemModel
from PyQt5.QtWidgets import *

from ..core import DynamicStringData, DynamicStringType
from ..core.constants import DYNAMIC_STRING_ROLE
from ..core.generators import file_func_generator
from ..ui import open_file
from ..ui.data_generator_dialog import DataGeneratorDialog
from ..ui.utility_functions_dialog import UtilityFunctionsDialog


class ChildLineEdit(QLineEdit):
    entry_completed = pyqtSignal(str, str, bool)

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
        self.entry_completed.emit(
            index.data(Qt.DisplayRole),
            index.data(DYNAMIC_STRING_ROLE),
            False
        )

    def focusOutEvent(self, e: QFocusEvent):
        if self.completer().popup().isVisible():
            self.entry_completed.emit("", "", True)

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Escape:
            self.entry_completed.emit("", "", True)
            e.ignore()

        super().keyPressEvent(e)


class CompletionContextMenuHandler:
    def __init__(self, view):
        self.view = view

    def setup_actions(self, menu):
        # Context Menu setup
        menu.addSeparator()

        enable_secret = QAction("Secret Hide/Show", self.view)
        enable_secret.triggered.connect(self.on_secret_value)

        data_dialog = QAction("Fake Data", self.view)
        data_dialog.triggered.connect(self.on_show_data_dialog)

        tools_dialog = QAction("Utility Functions", self.view)
        tools_dialog.triggered.connect(self.on_show_tools_dialog)

        menu.addActions([enable_secret, data_dialog, tools_dialog])

    def on_show_data_dialog(self):
        self.view.setup_selections()
        self.view.show_data_dialog(rollback=False)

    def on_show_tools_dialog(self):
        self.view.setup_selections()
        self.view.show_tools_dialog(rollback=False)

    def on_secret_value(self):
        dynamic_value: DynamicStringData = self.view.getValue()

        # Switch from secret -> plain, plain -> secret
        if self.view.echoMode() == QLineEdit.PasswordEchoOnEdit:
            dynamic_value.string_type = DynamicStringType.PLAIN.value
        else:
            dynamic_value.string_type = DynamicStringType.SECRET.value

        self.view.setValue(dynamic_value)


class CompletionLineEdit(QLineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.data_generator_dialog = DataGeneratorDialog(self)
        self.utility_functions_dialog = UtilityFunctionsDialog(self)
        self.child_edit = ChildLineEdit(self)
        self.child_edit.entry_completed.connect(self.pre_completion_check)
        self.selected_text = None
        self.selection_start = 0
        self.selection_length = 0

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        self.menu_item_handler = CompletionContextMenuHandler(self)

    def on_context_menu(self, position):
        menu = self.createStandardContextMenu()
        self.menu_item_handler.setup_actions(menu)
        menu.exec_(self.mapToGlobal(position))

    def show_data_dialog(self, rollback):
        cur_pos: QRect = self.cursorRect()
        global_position = self.mapToGlobal(cur_pos.bottomLeft())
        self.data_generator_dialog.move(global_position)
        if self.data_generator_dialog.exec_dialog() == QDialog.Accepted:
            f = self.data_generator_dialog.get_function()
            self.process_completion(f, f, rollback)
        else:
            self.process_completion(None, None, rollback=True)

    def show_tools_dialog(self, rollback):
        cur_pos: QRect = self.cursorRect()
        global_position = self.mapToGlobal(cur_pos.bottomLeft())
        self.utility_functions_dialog.move(global_position)
        if self.utility_functions_dialog.exec_dialog() == QDialog.Accepted:
            f = self.utility_functions_dialog.get_function()
            self.process_completion(f, f, rollback, replace_text=True)
        else:
            self.process_completion(None, None, rollback=True)

    def setup_selections(self):
        self.selected_text = self.selectedText()
        self.selection_start = self.selectionStart()
        self.selection_length = self.selectionLength()

    def pre_completion_check(self, text_in_field, variable_name, rollback=False):
        """Checks if one of the keyword is entered
        So that it can display appropriate dialog box
        Otherwise pass it to process completion
        """
        if text_in_field == "data":
            self.show_data_dialog(rollback)
        elif text_in_field == "tools":
            self.show_tools_dialog(rollback)
        elif text_in_field == "file":
            file_location, _ = open_file(self, "Select File")
            file_function = file_func_generator(file_location, wrap_in_quotes=True)
            self.process_completion(file_function, file_function, rollback)
        else:
            self.process_completion(text_in_field, variable_name, rollback)

    def process_completion(self, text_in_field, variable_name, rollback=False, replace_text=False):
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
                self.setup_selections()
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

        self.setText(new_val.value)

    def getValue(self):
        field_val = self.text().strip()
        string_type = DynamicStringType.PLAIN.value
        if self.echoMode() == QLineEdit.PasswordEchoOnEdit:
            string_type = DynamicStringType.SECRET.value

        return DynamicStringData(
            value=field_val,
            string_type=string_type
        )
