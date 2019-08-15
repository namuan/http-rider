# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/debug_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DebugWindow(object):
    def setupUi(self, DebugWindow):
        DebugWindow.setObjectName("DebugWindow")
        DebugWindow.resize(463, 266)
        self.centralwidget = QtWidgets.QWidget(DebugWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.txt_val = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_val.setGeometry(QtCore.QRect(100, 30, 221, 21))
        self.txt_val.setObjectName("txt_val")
        self.lbl_output = QtWidgets.QLabel(self.centralwidget)
        self.lbl_output.setGeometry(QtCore.QRect(40, 110, 351, 16))
        self.lbl_output.setObjectName("lbl_output")
        self.btn_test = QtWidgets.QPushButton(self.centralwidget)
        self.btn_test.setGeometry(QtCore.QRect(340, 30, 113, 32))
        self.btn_test.setObjectName("btn_test")
        self.btn_select = QtWidgets.QPushButton(self.centralwidget)
        self.btn_select.setGeometry(QtCore.QRect(180, 70, 113, 32))
        self.btn_select.setObjectName("btn_select")
        self.startVal = QtWidgets.QSpinBox(self.centralwidget)
        self.startVal.setGeometry(QtCore.QRect(70, 160, 48, 24))
        self.startVal.setObjectName("startVal")
        self.endVal = QtWidgets.QSpinBox(self.centralwidget)
        self.endVal.setGeometry(QtCore.QRect(140, 160, 48, 24))
        self.endVal.setObjectName("endVal")
        DebugWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DebugWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 463, 22))
        self.menubar.setObjectName("menubar")
        DebugWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DebugWindow)
        self.statusbar.setObjectName("statusbar")
        DebugWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DebugWindow)
        QtCore.QMetaObject.connectSlotsByName(DebugWindow)

    def retranslateUi(self, DebugWindow):
        _translate = QtCore.QCoreApplication.translate
        DebugWindow.setWindowTitle(_translate("DebugWindow", "MainWindow"))
        self.lbl_output.setText(_translate("DebugWindow", "TextLabel"))
        self.btn_test.setText(_translate("DebugWindow", "Test"))
        self.btn_select.setText(_translate("DebugWindow", "Select"))
