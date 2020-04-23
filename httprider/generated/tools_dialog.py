# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/tools_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UtilityFunctionsDialog(object):
    def setupUi(self, UtilityFunctionsDialog):
        UtilityFunctionsDialog.setObjectName("UtilityFunctionsDialog")
        UtilityFunctionsDialog.resize(422, 345)
        font = QtGui.QFont()
        font.setPointSize(10)
        UtilityFunctionsDialog.setFont(font)
        self.buttonBox = QtWidgets.QDialogButtonBox(UtilityFunctionsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(250, 310, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lbl_selected_text = QtWidgets.QLabel(UtilityFunctionsDialog)
        self.lbl_selected_text.setGeometry(QtCore.QRect(20, 10, 391, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.lbl_selected_text.setFont(font)
        self.lbl_selected_text.setObjectName("lbl_selected_text")
        self.function_selector = QtWidgets.QComboBox(UtilityFunctionsDialog)
        self.function_selector.setGeometry(QtCore.QRect(10, 80, 401, 26))
        self.function_selector.setObjectName("function_selector")
        self.btn_copy_transformed = QtWidgets.QToolButton(UtilityFunctionsDialog)
        self.btn_copy_transformed.setGeometry(QtCore.QRect(370, 110, 41, 22))
        self.btn_copy_transformed.setObjectName("btn_copy_transformed")
        self.txt_transformed_text = QtWidgets.QPlainTextEdit(UtilityFunctionsDialog)
        self.txt_transformed_text.setGeometry(QtCore.QRect(10, 110, 350, 181))
        self.txt_transformed_text.setObjectName("txt_transformed_text")

        self.retranslateUi(UtilityFunctionsDialog)
        self.buttonBox.accepted.connect(UtilityFunctionsDialog.accept)
        self.buttonBox.rejected.connect(UtilityFunctionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UtilityFunctionsDialog)

    def retranslateUi(self, UtilityFunctionsDialog):
        _translate = QtCore.QCoreApplication.translate
        UtilityFunctionsDialog.setWindowTitle(_translate("UtilityFunctionsDialog", "Dialog"))
        self.lbl_selected_text.setText(_translate("UtilityFunctionsDialog", "<selected text>"))
        self.btn_copy_transformed.setText(_translate("UtilityFunctionsDialog", "Copy"))
