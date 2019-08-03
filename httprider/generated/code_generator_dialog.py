# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/code_generator_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CodeGeneratorDialog(object):
    def setupUi(self, CodeGeneratorDialog):
        CodeGeneratorDialog.setObjectName("CodeGeneratorDialog")
        CodeGeneratorDialog.setWindowModality(QtCore.Qt.WindowModal)
        CodeGeneratorDialog.resize(953, 529)
        CodeGeneratorDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(CodeGeneratorDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cmb_exporters = QtWidgets.QComboBox(CodeGeneratorDialog)
        self.cmb_exporters.setObjectName("cmb_exporters")
        self.horizontalLayout.addWidget(self.cmb_exporters)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_copy_code = QtWidgets.QPushButton(CodeGeneratorDialog)
        self.btn_copy_code.setObjectName("btn_copy_code")
        self.horizontalLayout.addWidget(self.btn_copy_code)
        self.btn_export_code = QtWidgets.QPushButton(CodeGeneratorDialog)
        self.btn_export_code.setObjectName("btn_export_code")
        self.horizontalLayout.addWidget(self.btn_export_code)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.txt_generated_code = QtWidgets.QPlainTextEdit(CodeGeneratorDialog)
        self.txt_generated_code.setReadOnly(False)
        self.txt_generated_code.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.txt_generated_code.setObjectName("txt_generated_code")
        self.verticalLayout.addWidget(self.txt_generated_code)

        self.retranslateUi(CodeGeneratorDialog)
        QtCore.QMetaObject.connectSlotsByName(CodeGeneratorDialog)

    def retranslateUi(self, CodeGeneratorDialog):
        _translate = QtCore.QCoreApplication.translate
        CodeGeneratorDialog.setWindowTitle(_translate("CodeGeneratorDialog", "Dialog"))
        self.btn_copy_code.setText(_translate("CodeGeneratorDialog", "Copy"))
        self.btn_export_code.setText(_translate("CodeGeneratorDialog", "Export"))
