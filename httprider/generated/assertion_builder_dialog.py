# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/assertion_builder_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AssertionBuilderDialog(object):
    def setupUi(self, AssertionBuilderDialog):
        AssertionBuilderDialog.setObjectName("AssertionBuilderDialog")
        AssertionBuilderDialog.setWindowModality(QtCore.Qt.WindowModal)
        AssertionBuilderDialog.resize(1203, 723)
        AssertionBuilderDialog.setModal(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(AssertionBuilderDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter_2 = QtWidgets.QSplitter(AssertionBuilderDialog)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.frame = QtWidgets.QFrame(self.splitter)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tbl_request_headers = QtWidgets.QTreeWidget(self.frame)
        self.tbl_request_headers.setObjectName("tbl_request_headers")
        self.tbl_request_headers.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.tbl_request_headers.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.tbl_request_headers)
        self.tbl_request_body = QtWidgets.QTreeView(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.tbl_request_body.sizePolicy().hasHeightForWidth()
        )
        self.tbl_request_body.setSizePolicy(sizePolicy)
        self.tbl_request_body.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.tbl_request_body.setObjectName("tbl_request_body")
        self.tbl_request_body.header().setVisible(False)
        self.tbl_request_body.header().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tbl_request_body)
        self.frame_2 = QtWidgets.QFrame(self.splitter)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.tbl_response_headers = QtWidgets.QTreeWidget(self.frame_2)
        self.tbl_response_headers.setObjectName("tbl_response_headers")
        self.tbl_response_headers.headerItem().setTextAlignment(
            0, QtCore.Qt.AlignCenter
        )
        self.tbl_response_headers.headerItem().setTextAlignment(
            1, QtCore.Qt.AlignCenter
        )
        self.verticalLayout_2.addWidget(self.tbl_response_headers)
        self.tbl_response_body = QtWidgets.QTreeView(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.tbl_response_body.sizePolicy().hasHeightForWidth()
        )
        self.tbl_response_body.setSizePolicy(sizePolicy)
        self.tbl_response_body.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.tbl_response_body.setObjectName("tbl_response_body")
        self.tbl_response_body.header().setVisible(False)
        self.tbl_response_body.header().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.tbl_response_body)
        self.frame_3 = QtWidgets.QFrame(self.splitter_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_response_code_assertion = QtWidgets.QToolButton(self.frame_3)
        self.btn_response_code_assertion.setObjectName("btn_response_code_assertion")
        self.horizontalLayout_2.addWidget(self.btn_response_code_assertion)
        self.btn_response_time_assertion = QtWidgets.QToolButton(self.frame_3)
        self.btn_response_time_assertion.setObjectName("btn_response_time_assertion")
        self.horizontalLayout_2.addWidget(self.btn_response_time_assertion)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.tbl_assertions = QtWidgets.QTreeWidget(self.frame_3)
        self.tbl_assertions.setObjectName("tbl_assertions")
        self.tbl_assertions.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.tbl_assertions.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.tbl_assertions.headerItem().setTextAlignment(2, QtCore.Qt.AlignCenter)
        self.tbl_assertions.headerItem().setTextAlignment(3, QtCore.Qt.AlignCenter)
        self.tbl_assertions.headerItem().setTextAlignment(4, QtCore.Qt.AlignCenter)
        self.tbl_assertions.headerItem().setTextAlignment(5, QtCore.Qt.AlignCenter)
        self.tbl_assertions.headerItem().setTextAlignment(6, QtCore.Qt.AlignCenter)
        self.tbl_assertions.header().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.tbl_assertions)
        self.horizontalLayout.addWidget(self.splitter_2)

        self.retranslateUi(AssertionBuilderDialog)
        QtCore.QMetaObject.connectSlotsByName(AssertionBuilderDialog)

    def retranslateUi(self, AssertionBuilderDialog):
        _translate = QtCore.QCoreApplication.translate
        AssertionBuilderDialog.setWindowTitle(
            _translate("AssertionBuilderDialog", "Assertions Builder")
        )
        self.label.setText(_translate("AssertionBuilderDialog", "Request"))
        self.tbl_request_headers.headerItem().setText(
            0, _translate("AssertionBuilderDialog", "Name")
        )
        self.tbl_request_headers.headerItem().setText(
            1, _translate("AssertionBuilderDialog", "Value")
        )
        self.label_2.setText(_translate("AssertionBuilderDialog", "Response"))
        self.tbl_response_headers.headerItem().setText(
            0, _translate("AssertionBuilderDialog", "Name")
        )
        self.tbl_response_headers.headerItem().setText(
            1, _translate("AssertionBuilderDialog", "Value")
        )
        self.label_3.setText(_translate("AssertionBuilderDialog", "Assertions"))
        self.btn_response_code_assertion.setText(
            _translate("AssertionBuilderDialog", "HTTP 200")
        )
        self.btn_response_time_assertion.setText(
            _translate("AssertionBuilderDialog", "317 ms")
        )
        self.tbl_assertions.headerItem().setText(
            0, _translate("AssertionBuilderDialog", "From")
        )
        self.tbl_assertions.headerItem().setText(
            1, _translate("AssertionBuilderDialog", "Name")
        )
        self.tbl_assertions.headerItem().setText(
            2, _translate("AssertionBuilderDialog", "Selector")
        )
        self.tbl_assertions.headerItem().setText(
            3, _translate("AssertionBuilderDialog", "Current Value")
        )
        self.tbl_assertions.headerItem().setText(
            4, _translate("AssertionBuilderDialog", "Matcher")
        )
        self.tbl_assertions.headerItem().setText(
            5, _translate("AssertionBuilderDialog", "Expected Value")
        )
        self.tbl_assertions.headerItem().setText(
            6, _translate("AssertionBuilderDialog", "X")
        )
