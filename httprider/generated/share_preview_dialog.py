# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/share_preview_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SharePreviewDialog(object):
    def setupUi(self, SharePreviewDialog):
        SharePreviewDialog.setObjectName("SharePreviewDialog")
        SharePreviewDialog.setWindowModality(QtCore.Qt.WindowModal)
        SharePreviewDialog.resize(984, 468)
        SharePreviewDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(SharePreviewDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(SharePreviewDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_show_preview = QtWidgets.QPushButton(SharePreviewDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_show_preview.setFont(font)
        self.btn_show_preview.setObjectName("btn_show_preview")
        self.horizontalLayout.addWidget(self.btn_show_preview)
        self.btn_export_code = QtWidgets.QPushButton(SharePreviewDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_export_code.setFont(font)
        self.btn_export_code.setObjectName("btn_export_code")
        self.horizontalLayout.addWidget(self.btn_export_code)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.txt_preview_share = QtWidgets.QTextEdit(SharePreviewDialog)
        self.txt_preview_share.setObjectName("txt_preview_share")
        self.verticalLayout.addWidget(self.txt_preview_share)

        self.retranslateUi(SharePreviewDialog)
        QtCore.QMetaObject.connectSlotsByName(SharePreviewDialog)

    def retranslateUi(self, SharePreviewDialog):
        _translate = QtCore.QCoreApplication.translate
        SharePreviewDialog.setWindowTitle(_translate("SharePreviewDialog", "Dialog"))
        self.label.setText(_translate("SharePreviewDialog", "Review the following request/response but note that any changes made in the preview will be discarded when the dialog is closed."))
        self.btn_show_preview.setText(_translate("SharePreviewDialog", "Preview"))
        self.btn_export_code.setText(_translate("SharePreviewDialog", "Share"))
