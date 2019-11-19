# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/debug_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DebugWindow(object):
    def setupUi(self, DebugWindow):
        DebugWindow.setObjectName("DebugWindow")
        DebugWindow.resize(622, 498)
        self.centralwidget = QtWidgets.QWidget(DebugWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(70, 80, 302, 255))
        self.tabWidget.setStyleSheet("QTabWidget::pane {\n"
"    border: 1px solid black;\n"
"    background: white;\n"
"}")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.tab)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout.addWidget(self.plainTextEdit)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        DebugWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DebugWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 622, 22))
        self.menubar.setObjectName("menubar")
        DebugWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DebugWindow)
        self.statusbar.setObjectName("statusbar")
        DebugWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DebugWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DebugWindow)

    def retranslateUi(self, DebugWindow):
        _translate = QtCore.QCoreApplication.translate
        DebugWindow.setWindowTitle(_translate("DebugWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("DebugWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("DebugWindow", "Tab 2"))
