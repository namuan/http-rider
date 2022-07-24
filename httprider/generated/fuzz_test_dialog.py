# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/fuzz_test_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FuzzTestDialog(object):
    def setupUi(self, FuzzTestDialog):
        FuzzTestDialog.setObjectName("FuzzTestDialog")
        FuzzTestDialog.setWindowModality(QtCore.Qt.WindowModal)
        FuzzTestDialog.resize(739, 499)
        font = QtGui.QFont()
        font.setPointSize(10)
        FuzzTestDialog.setFont(font)
        FuzzTestDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(FuzzTestDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lbl_api_call = QtWidgets.QLabel(FuzzTestDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lbl_api_call.setFont(font)
        self.lbl_api_call.setObjectName("lbl_api_call")
        self.horizontalLayout_2.addWidget(self.lbl_api_call)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem)
        self.line_2 = QtWidgets.QFrame(FuzzTestDialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.lbl_fuzz_results = QtWidgets.QLabel(FuzzTestDialog)
        self.lbl_fuzz_results.setObjectName("lbl_fuzz_results")
        self.horizontalLayout_2.addWidget(self.lbl_fuzz_results)
        self.btn_fuzz_test = QtWidgets.QPushButton(FuzzTestDialog)
        self.btn_fuzz_test.setObjectName("btn_fuzz_test")
        self.horizontalLayout_2.addWidget(self.btn_fuzz_test)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(FuzzTestDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.int_fuzz_count = QtWidgets.QSpinBox(FuzzTestDialog)
        self.int_fuzz_count.setMinimum(2)
        self.int_fuzz_count.setSingleStep(2)
        self.int_fuzz_count.setProperty("value", 2)
        self.int_fuzz_count.setObjectName("int_fuzz_count")
        self.horizontalLayout.addWidget(self.int_fuzz_count)
        self.line_3 = QtWidgets.QFrame(FuzzTestDialog)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout.addWidget(self.line_3)
        self.label = QtWidgets.QLabel(FuzzTestDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.int_max_array_items = QtWidgets.QSpinBox(FuzzTestDialog)
        self.int_max_array_items.setSingleStep(5)
        self.int_max_array_items.setProperty("value", 10)
        self.int_max_array_items.setObjectName("int_max_array_items")
        self.horizontalLayout.addWidget(self.int_max_array_items)
        self.line = QtWidgets.QFrame(FuzzTestDialog)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.label_2 = QtWidgets.QLabel(FuzzTestDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.int_max_string_length = QtWidgets.QSpinBox(FuzzTestDialog)
        self.int_max_string_length.setMaximum(500)
        self.int_max_string_length.setSingleStep(10)
        self.int_max_string_length.setProperty("value", 250)
        self.int_max_string_length.setObjectName("int_max_string_length")
        self.horizontalLayout.addWidget(self.int_max_string_length)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem1)
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
        self.label_3.setText(_translate("FuzzTestDialog", "Iterations"))
        self.label.setText(_translate("FuzzTestDialog", "Max array items"))
        self.label_2.setText(_translate("FuzzTestDialog", "Max string length"))
