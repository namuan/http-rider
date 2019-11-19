# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/tag_info_widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TagInfoWidget(object):
    def setupUi(self, TagInfoWidget):
        TagInfoWidget.setObjectName("TagInfoWidget")
        TagInfoWidget.resize(516, 165)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TagInfoWidget.sizePolicy().hasHeightForWidth())
        TagInfoWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(TagInfoWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(5, 1, 5, 1)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_tag = QtWidgets.QLabel(TagInfoWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_tag.sizePolicy().hasHeightForWidth())
        self.lbl_tag.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_tag.setFont(font)
        self.lbl_tag.setTextFormat(QtCore.Qt.AutoText)
        self.lbl_tag.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_tag.setWordWrap(True)
        self.lbl_tag.setObjectName("lbl_tag")
        self.gridLayout.addWidget(self.lbl_tag, 0, 0, 1, 1)
        self.txt_tag_info = QtWidgets.QPlainTextEdit(TagInfoWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_tag_info.sizePolicy().hasHeightForWidth())
        self.txt_tag_info.setSizePolicy(sizePolicy)
        self.txt_tag_info.setObjectName("txt_tag_info")
        self.gridLayout.addWidget(self.txt_tag_info, 0, 1, 1, 1)
        self.gridLayout.setColumnMinimumWidth(0, 150)
        self.gridLayout.setColumnStretch(1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(TagInfoWidget)
        QtCore.QMetaObject.connectSlotsByName(TagInfoWidget)

    def retranslateUi(self, TagInfoWidget):
        _translate = QtCore.QCoreApplication.translate
        TagInfoWidget.setWindowTitle(_translate("TagInfoWidget", "Form"))
        self.lbl_tag.setText(_translate("TagInfoWidget", "Registration Auth"))
