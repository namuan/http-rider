# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/new_item_widget.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_NewItemWidget(object):
    def setupUi(self, NewItemWidget):
        NewItemWidget.setObjectName("NewItemWidget")
        NewItemWidget.resize(417, 44)
        self.horizontalLayout = QtWidgets.QHBoxLayout(NewItemWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_new_header = QtWidgets.QPushButton(NewItemWidget)
        self.btn_new_header.setObjectName("btn_new_header")
        self.horizontalLayout.addWidget(self.btn_new_header)

        self.retranslateUi(NewItemWidget)
        QtCore.QMetaObject.connectSlotsByName(NewItemWidget)

    def retranslateUi(self, NewItemWidget):
        _translate = QtCore.QCoreApplication.translate
        NewItemWidget.setWindowTitle(_translate("NewItemWidget", "Form"))
        self.btn_new_header.setText(_translate("NewItemWidget", "Add New"))


