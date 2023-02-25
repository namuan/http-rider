from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QTextCursor, QKeyEvent, QTextCharFormat
from PyQt6.QtWidgets import QPlainTextEdit, QDialog
from PyQt6.QtGui import QAction
from ..ui.data_generator_dialog import DataGeneratorDialog
from ..ui.utility_functions_dialog import UtilityFunctionsDialog
from ..widgets.completion_line_edit import ChildLineEdit


class PlainTextContextMenuHandler:
    def __init__(self, view):
        self.view = view

    def setup_actions(self, menu):
        # Context Menu setup
        menu.addSeparator()

        data_dialog = QAction("Fake Data", self.view)
        data_dialog.triggered.connect(self.on_show_data_dialog)

        tools_dialog = QAction("Utility Functions", self.view)
        tools_dialog.triggered.connect(self.on_show_tools_dialog)

        menu.addActions([data_dialog, tools_dialog])

    def on_show_data_dialog(self):
        self.view.setup_selections()
        self.view.show_data_dialog(rollback=False)

    def on_show_tools_dialog(self):
        self.view.setup_selections()
        self.view.show_tools_dialog(rollback=False)


class CompletionPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data_generator_dialog = DataGeneratorDialog(self)
        self.utility_functions_dialog = UtilityFunctionsDialog(self)
        self.child_edit = ChildLineEdit(self)
        self.child_edit.entry_completed.connect(self.pre_completion_check)
        self.selected_text = None
        self.selection_start = 0
        self.selection_end = 0

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        self.menu_item_handler = PlainTextContextMenuHandler(self)

    def text(self):
        return None

    def on_context_menu(self, position):
        menu = self.createStandardContextMenu()
        self.menu_item_handler.setup_actions(menu)
        menu.exec(self.mapToGlobal(position))

    def setup_selections(self):
        tc: QTextCursor = self.textCursor()
        self.selected_text = tc.selectedText()
        self.selection_start = tc.selectionStart()
        self.selection_end = tc.selectionEnd()

    def show_data_dialog(self, rollback):
        cur_pos: QRect = self.cursorRect()
        global_position = self.mapToGlobal(cur_pos.bottomLeft())
        self.data_generator_dialog.move(global_position)
        if self.data_generator_dialog.execdialog() == QDialog.DialogCode.Accepted:
            f = self.data_generator_dialog.get_function()
            self.process_completion(f, f, rollback)
        else:
            self.process_completion(None, None, rollback=True)

    def show_tools_dialog(self, rollback):
        cur_pos: QRect = self.cursorRect()
        global_position = self.mapToGlobal(cur_pos.bottomLeft())
        self.utility_functions_dialog.move(global_position)
        if self.utility_functions_dialog.execdialog() == QDialog.DialogCode.Accepted:
            f = self.utility_functions_dialog.get_function()
            self.process_completion(f, f, rollback)
        else:
            self.process_completion(None, None, rollback=True)

    def pre_completion_check(self, text_in_field, variable_name, rollback=False):
        """Checks if one of the keyword is entered
        So that it can display appropriate dialog box
        Otherwise pass it to process completion
        """
        if text_in_field == "data":
            self.show_data_dialog(rollback)
        elif text_in_field == "tools":
            self.show_tools_dialog(rollback)
        else:
            self.process_completion(text_in_field, variable_name, rollback)

    def process_completion(self, text_in_field, variable_name, rollback=False):
        self.child_edit.completer().popup().hide()
        self.child_edit.hide()
        self.child_edit.setText("")

        self.setFocus(Qt.FocusReason.OtherFocusReason)
        if not rollback:
            if self.selected_text:
                tc: QTextCursor = self.textCursor()
                tc.setPosition(self.selection_start)
                tc.setPosition(self.selection_end, QTextCursor.MoveOperation.KeepAnchor)
                self.setTextCursor(tc)

            existing_format = self.currentCharFormat()
            tf: QTextCharFormat = QTextCharFormat()
            tf.setToolTip(text_in_field)
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
        if e.key() == Qt.Key.Key_Dollar:
            if not popup_visible:
                tc: QTextCursor = self.textCursor()
                self.selected_text = tc.selectedText()
                self.selection_start = tc.selectionStart()
                self.selection_end = tc.selectionEnd()
                tc.setPosition(tc.selectionStart())
                self.setTextCursor(tc)
                popup_rect = self.boundingRect()
                self.child_edit.setGeometry(popup_rect)
                self.child_edit.setText("")
                self.child_edit.show()
                self.child_edit.setFocus(Qt.FocusReason.OtherFocusReason)
                return

        super().keyPressEvent(e)
