# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/configuration_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Configuration(object):
    def setupUi(self, Configuration):
        Configuration.setObjectName("Configuration")
        Configuration.setWindowModality(QtCore.Qt.WindowModal)
        Configuration.resize(486, 255)
        Configuration.setModal(True)
        self.tabWidget = QtWidgets.QTabWidget(Configuration)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 451, 191))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.txt_http_proxy = QtWidgets.QLineEdit(self.tab)
        self.txt_http_proxy.setObjectName("txt_http_proxy")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_http_proxy)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.txt_https_proxy = QtWidgets.QLineEdit(self.tab)
        self.txt_https_proxy.setObjectName("txt_https_proxy")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_https_proxy)
        self.chk_tls_verficiation = QtWidgets.QCheckBox(self.tab)
        self.chk_tls_verficiation.setChecked(True)
        self.chk_tls_verficiation.setObjectName("chk_tls_verficiation")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.chk_tls_verficiation)
        self.horizontalLayout.addLayout(self.formLayout)
        self.tabWidget.addTab(self.tab, "")
        self.update = QtWidgets.QWidget()
        self.update.setObjectName("update")
        self.chk_updates_startup = QtWidgets.QCheckBox(self.update)
        self.chk_updates_startup.setGeometry(QtCore.QRect(20, 20, 221, 20))
        self.chk_updates_startup.setChecked(True)
        self.chk_updates_startup.setObjectName("chk_updates_startup")
        self.tabWidget.addTab(self.update, "")
        self.btn_save_configuration = QtWidgets.QPushButton(Configuration)
        self.btn_save_configuration.setGeometry(QtCore.QRect(360, 210, 113, 32))
        self.btn_save_configuration.setObjectName("btn_save_configuration")
        self.btn_cancel_configuration = QtWidgets.QPushButton(Configuration)
        self.btn_cancel_configuration.setGeometry(QtCore.QRect(250, 210, 113, 32))
        self.btn_cancel_configuration.setObjectName("btn_cancel_configuration")

        self.retranslateUi(Configuration)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Configuration)

    def retranslateUi(self, Configuration):
        _translate = QtCore.QCoreApplication.translate
        Configuration.setWindowTitle(_translate("Configuration", "Settings"))
        self.label.setText(_translate("Configuration", "http"))
        self.label_2.setText(_translate("Configuration", "https"))
        self.chk_tls_verficiation.setText(_translate("Configuration", "SSL/TLS verification"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Configuration", "HTTP Proxy"))
        self.chk_updates_startup.setText(_translate("Configuration", "Check for updates on start up"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.update), _translate("Configuration", "Updates"))
        self.btn_save_configuration.setText(_translate("Configuration", "OK"))
        self.btn_cancel_configuration.setText(_translate("Configuration", "Cancel"))
