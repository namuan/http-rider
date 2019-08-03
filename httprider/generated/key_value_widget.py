# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/key_value_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_KeyValueWidget(object):
    def setupUi(self, KeyValueWidget):
        KeyValueWidget.setObjectName("KeyValueWidget")
        KeyValueWidget.resize(473, 32)
        KeyValueWidget.setStyleSheet("")
        self.horizontalLayout = QtWidgets.QHBoxLayout(KeyValueWidget)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chk_field_enabled = QtWidgets.QCheckBox(KeyValueWidget)
        self.chk_field_enabled.setText("")
        self.chk_field_enabled.setChecked(True)
        self.chk_field_enabled.setObjectName("chk_field_enabled")
        self.horizontalLayout.addWidget(self.chk_field_enabled)
        self.txt_name = QtWidgets.QLineEdit(KeyValueWidget)
        self.txt_name.setStyleSheet("")
        self.txt_name.setObjectName("txt_name")
        self.horizontalLayout.addWidget(self.txt_name)
        self.txt_value = CompletionLineEdit(KeyValueWidget)
        self.txt_value.setObjectName("txt_value")
        self.horizontalLayout.addWidget(self.txt_value)
        self.btn_remove_header = QtWidgets.QToolButton(KeyValueWidget)
        self.btn_remove_header.setObjectName("btn_remove_header")
        self.horizontalLayout.addWidget(self.btn_remove_header)

        self.retranslateUi(KeyValueWidget)
        QtCore.QMetaObject.connectSlotsByName(KeyValueWidget)

    def retranslateUi(self, KeyValueWidget):
        _translate = QtCore.QCoreApplication.translate
        KeyValueWidget.setWindowTitle(_translate("KeyValueWidget", "Form"))
        self.btn_remove_header.setText(_translate("KeyValueWidget", "-"))
from ..widgets.completion_line_edit import CompletionLineEdit
