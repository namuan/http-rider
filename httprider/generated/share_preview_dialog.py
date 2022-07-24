# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/share_preview_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SharePreviewDialog(object):
    def setupUi(self, SharePreviewDialog):
        SharePreviewDialog.setObjectName("SharePreviewDialog")
        SharePreviewDialog.setWindowModality(QtCore.Qt.WindowModal)
        SharePreviewDialog.resize(1010, 468)
        SharePreviewDialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(SharePreviewDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(SharePreviewDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.btn_show_preview = QtWidgets.QPushButton(SharePreviewDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_show_preview.setFont(font)
        self.btn_show_preview.setObjectName("btn_show_preview")
        self.horizontalLayout.addWidget(self.btn_show_preview)
        self.btn_share_exchange = QtWidgets.QPushButton(SharePreviewDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_share_exchange.setFont(font)
        self.btn_share_exchange.setObjectName("btn_share_exchange")
        self.horizontalLayout.addWidget(self.btn_share_exchange)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lbl_share_location = QtWidgets.QLabel(SharePreviewDialog)
        self.lbl_share_location.setTextFormat(QtCore.Qt.RichText)
        self.lbl_share_location.setOpenExternalLinks(True)
        self.lbl_share_location.setObjectName("lbl_share_location")
        self.verticalLayout.addWidget(self.lbl_share_location)
        self.txt_preview_share = QtWidgets.QTextEdit(SharePreviewDialog)
        self.txt_preview_share.setObjectName("txt_preview_share")
        self.verticalLayout.addWidget(self.txt_preview_share)

        self.retranslateUi(SharePreviewDialog)
        QtCore.QMetaObject.connectSlotsByName(SharePreviewDialog)

    def retranslateUi(self, SharePreviewDialog):
        _translate = QtCore.QCoreApplication.translate
        SharePreviewDialog.setWindowTitle(_translate("SharePreviewDialog", "Dialog"))
        self.label.setText(
            _translate(
                "SharePreviewDialog",
                "Review/Edit the following request/response but note that any changes made in the preview will be discarded when the dialog is closed.",
            )
        )
        self.btn_show_preview.setText(_translate("SharePreviewDialog", "Preview"))
        self.btn_share_exchange.setText(_translate("SharePreviewDialog", "Share"))
        self.lbl_share_location.setText(
            _translate("SharePreviewDialog", "Share location will appear here")
        )
