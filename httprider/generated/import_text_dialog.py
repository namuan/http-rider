# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/import_text_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ImportTextDialog(object):
    def setupUi(self, ImportTextDialog):
        ImportTextDialog.setObjectName("ImportTextDialog")
        ImportTextDialog.setWindowModality(QtCore.Qt.WindowModal)
        ImportTextDialog.resize(547, 329)
        ImportTextDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(ImportTextDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.txt_import = QtWidgets.QPlainTextEdit(ImportTextDialog)
        self.txt_import.setObjectName("txt_import")
        self.verticalLayout.addWidget(self.txt_import)
        self.lbl_error_message = QtWidgets.QLabel(ImportTextDialog)
        self.lbl_error_message.setObjectName("lbl_error_message")
        self.verticalLayout.addWidget(self.lbl_error_message)
        self.btn_dialog_buttons = QtWidgets.QDialogButtonBox(ImportTextDialog)
        self.btn_dialog_buttons.setOrientation(QtCore.Qt.Horizontal)
        self.btn_dialog_buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btn_dialog_buttons.setObjectName("btn_dialog_buttons")
        self.verticalLayout.addWidget(self.btn_dialog_buttons)

        self.retranslateUi(ImportTextDialog)
        self.btn_dialog_buttons.accepted.connect(ImportTextDialog.accept)
        self.btn_dialog_buttons.rejected.connect(ImportTextDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ImportTextDialog)

    def retranslateUi(self, ImportTextDialog):
        _translate = QtCore.QCoreApplication.translate
        ImportTextDialog.setWindowTitle(_translate("ImportTextDialog", "Dialog"))
        self.lbl_error_message.setText(_translate("ImportTextDialog", "TextLabel"))
