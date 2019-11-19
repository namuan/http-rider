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
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_copy_code = QtWidgets.QPushButton(FuzzTestDialog)
        self.btn_copy_code.setObjectName("btn_copy_code")
        self.horizontalLayout.addWidget(self.btn_copy_code)
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
        self.btn_copy_code.setText(_translate("FuzzTestDialog", "Test"))
