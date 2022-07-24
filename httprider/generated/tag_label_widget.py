# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/tag_label_widget.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TagLabelWidget(object):
    def setupUi(self, TagLabelWidget):
        TagLabelWidget.setObjectName("TagLabelWidget")
        TagLabelWidget.resize(194, 36)
        font = QtGui.QFont()
        font.setPointSize(10)
        TagLabelWidget.setFont(font)
        self.frame = QtWidgets.QFrame(TagLabelWidget)
        self.frame.setGeometry(QtCore.QRect(1, 1, 190, 31))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 191, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_tag_remove = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.btn_tag_remove.setObjectName("btn_tag_remove")
        self.horizontalLayout.addWidget(self.btn_tag_remove)

        self.retranslateUi(TagLabelWidget)
        QtCore.QMetaObject.connectSlotsByName(TagLabelWidget)

    def retranslateUi(self, TagLabelWidget):
        _translate = QtCore.QCoreApplication.translate
        TagLabelWidget.setWindowTitle(_translate("TagLabelWidget", "Form"))
        self.btn_tag_remove.setText(_translate("TagLabelWidget", "X"))
