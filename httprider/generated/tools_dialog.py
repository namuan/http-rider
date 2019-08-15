# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/tools_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UtilityFunctionsDialog(object):
    def setupUi(self, UtilityFunctionsDialog):
        UtilityFunctionsDialog.setObjectName("UtilityFunctionsDialog")
        UtilityFunctionsDialog.resize(422, 345)
        self.buttonBox = QtWidgets.QDialogButtonBox(UtilityFunctionsDialog)
        self.buttonBox.setGeometry(QtCore.QRect(70, 310, 341, 32))
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
        self.function_selector.setGeometry(QtCore.QRect(10, 70, 391, 26))
        self.function_selector.setObjectName("function_selector")
        self.lbl_transformed_text = QtWidgets.QLabel(UtilityFunctionsDialog)
        self.lbl_transformed_text.setGeometry(QtCore.QRect(20, 190, 331, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.lbl_transformed_text.setFont(font)
        self.lbl_transformed_text.setObjectName("lbl_transformed_text")

        self.retranslateUi(UtilityFunctionsDialog)
        self.buttonBox.accepted.connect(UtilityFunctionsDialog.accept)
        self.buttonBox.rejected.connect(UtilityFunctionsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UtilityFunctionsDialog)

    def retranslateUi(self, UtilityFunctionsDialog):
        _translate = QtCore.QCoreApplication.translate
        UtilityFunctionsDialog.setWindowTitle(_translate("UtilityFunctionsDialog", "Dialog"))
        self.lbl_selected_text.setText(_translate("UtilityFunctionsDialog", "<selected text>"))
        self.lbl_transformed_text.setText(_translate("UtilityFunctionsDialog", "<transformed value>"))
