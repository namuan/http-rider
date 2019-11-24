# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/fuzz_test_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FuzzTestDialog(object):
    def setupUi(self, FuzzTestDialog):
        FuzzTestDialog.setObjectName("FuzzTestDialog")
        FuzzTestDialog.setWindowModality(QtCore.Qt.WindowModal)
        FuzzTestDialog.resize(953, 529)
        FuzzTestDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(FuzzTestDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txt_fuzz_count = QtWidgets.QSpinBox(FuzzTestDialog)
        self.txt_fuzz_count.setMinimum(5)
        self.txt_fuzz_count.setSingleStep(5)
        self.txt_fuzz_count.setProperty("value", 5)
        self.txt_fuzz_count.setObjectName("txt_fuzz_count")
        self.horizontalLayout.addWidget(self.txt_fuzz_count)
        self.lbl_api_call = QtWidgets.QLabel(FuzzTestDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lbl_api_call.setFont(font)
        self.lbl_api_call.setObjectName("lbl_api_call")
        self.horizontalLayout.addWidget(self.lbl_api_call)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lbl_fuzz_results = QtWidgets.QLabel(FuzzTestDialog)
        self.lbl_fuzz_results.setObjectName("lbl_fuzz_results")
        self.horizontalLayout.addWidget(self.lbl_fuzz_results)
        self.btn_fuzz_test = QtWidgets.QPushButton(FuzzTestDialog)
        self.btn_fuzz_test.setObjectName("btn_fuzz_test")
        self.horizontalLayout.addWidget(self.btn_fuzz_test)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.txt_fuzz_output = QtWidgets.QPlainTextEdit(FuzzTestDialog)
        self.txt_fuzz_output.setReadOnly(False)
        self.txt_fuzz_output.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.txt_fuzz_output.setObjectName("txt_fuzz_output")
        self.verticalLayout.addWidget(self.txt_fuzz_output)

        self.retranslateUi(FuzzTestDialog)
        QtCore.QMetaObject.connectSlotsByName(FuzzTestDialog)

    def retranslateUi(self, FuzzTestDialog):
        _translate = QtCore.QCoreApplication.translate
        FuzzTestDialog.setWindowTitle(_translate("FuzzTestDialog", "Dialog"))
        self.lbl_api_call.setText(_translate("FuzzTestDialog", "TextLabel"))
        self.lbl_fuzz_results.setText(_translate("FuzzTestDialog", "Results"))
        self.btn_fuzz_test.setText(_translate("FuzzTestDialog", "Test"))
