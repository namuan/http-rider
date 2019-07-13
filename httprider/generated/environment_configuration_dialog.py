# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/environment_configuration_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EnvironmentsConfigurationDialog(object):
    def setupUi(self, EnvironmentsConfigurationDialog):
        EnvironmentsConfigurationDialog.setObjectName("EnvironmentsConfigurationDialog")
        EnvironmentsConfigurationDialog.setWindowModality(QtCore.Qt.WindowModal)
        EnvironmentsConfigurationDialog.resize(1020, 820)
        EnvironmentsConfigurationDialog.setModal(True)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(EnvironmentsConfigurationDialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.splitter = QtWidgets.QSplitter(EnvironmentsConfigurationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.frame = QtWidgets.QFrame(self.splitter)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_duplicate_environment = QtWidgets.QToolButton(self.frame)
        self.btn_duplicate_environment.setObjectName("btn_duplicate_environment")
        self.horizontalLayout.addWidget(self.btn_duplicate_environment)
        self.btn_remove_environment = QtWidgets.QToolButton(self.frame)
        self.btn_remove_environment.setObjectName("btn_remove_environment")
        self.horizontalLayout.addWidget(self.btn_remove_environment)
        self.btn_add_environment = QtWidgets.QToolButton(self.frame)
        self.btn_add_environment.setObjectName("btn_add_environment")
        self.horizontalLayout.addWidget(self.btn_add_environment)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lst_environments = QtWidgets.QListWidget(self.frame)
        self.lst_environments.setAlternatingRowColors(False)
        self.lst_environments.setObjectName("lst_environments")
        self.verticalLayout.addWidget(self.lst_environments)
        self.lst_environment_data = QtWidgets.QListWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lst_environment_data.sizePolicy().hasHeightForWidth())
        self.lst_environment_data.setSizePolicy(sizePolicy)
        self.lst_environment_data.setObjectName("lst_environment_data")
        self.horizontalLayout_2.addWidget(self.splitter)

        self.retranslateUi(EnvironmentsConfigurationDialog)
        QtCore.QMetaObject.connectSlotsByName(EnvironmentsConfigurationDialog)

    def retranslateUi(self, EnvironmentsConfigurationDialog):
        _translate = QtCore.QCoreApplication.translate
        EnvironmentsConfigurationDialog.setWindowTitle(_translate("EnvironmentsConfigurationDialog", "Environments"))
        self.btn_duplicate_environment.setText(_translate("EnvironmentsConfigurationDialog", "++"))
        self.btn_remove_environment.setText(_translate("EnvironmentsConfigurationDialog", "-"))
        self.btn_add_environment.setText(_translate("EnvironmentsConfigurationDialog", "+"))


