# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/progress_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName("ProgressDialog")
        ProgressDialog.setWindowModality(QtCore.Qt.WindowModal)
        ProgressDialog.setEnabled(True)
        ProgressDialog.resize(382, 109)
        ProgressDialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        ProgressDialog.setModal(True)
        self.lbl_progress_status = QtWidgets.QLabel(ProgressDialog)
        self.lbl_progress_status.setGeometry(QtCore.QRect(30, 30, 331, 16))
        self.lbl_progress_status.setText("")
        self.lbl_progress_status.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_progress_status.setObjectName("lbl_progress_status")
        self.btn_cancel_progress = QtWidgets.QPushButton(ProgressDialog)
        self.btn_cancel_progress.setGeometry(QtCore.QRect(140, 70, 113, 32))
        self.btn_cancel_progress.setObjectName("btn_cancel_progress")

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        _translate = QtCore.QCoreApplication.translate
        ProgressDialog.setWindowTitle(_translate("ProgressDialog", "Progress ..."))
        self.btn_cancel_progress.setText(_translate("ProgressDialog", "Cancel"))


