# Form implementation generated from reading ui file 'resources/ui/debug_window.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DebugWindow(object):
    def setupUi(self, DebugWindow):
        DebugWindow.setObjectName("DebugWindow")
        DebugWindow.resize(622, 498)
        self.centralwidget = QtWidgets.QWidget(parent=DebugWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = ExampleOverlayedText(parent=self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        DebugWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=DebugWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 622, 22))
        self.menubar.setObjectName("menubar")
        DebugWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=DebugWindow)
        self.statusbar.setObjectName("statusbar")
        DebugWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DebugWindow)
        QtCore.QMetaObject.connectSlotsByName(DebugWindow)

    def retranslateUi(self, DebugWindow):
        _translate = QtCore.QCoreApplication.translate
        DebugWindow.setWindowTitle(_translate("DebugWindow", "MainWindow"))
from example_overlayed_text import ExampleOverlayedText
