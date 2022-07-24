# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/ui/project_info_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProjectInfoDialog(object):
    def setupUi(self, ProjectInfoDialog):
        ProjectInfoDialog.setObjectName("ProjectInfoDialog")
        ProjectInfoDialog.setWindowModality(QtCore.Qt.WindowModal)
        ProjectInfoDialog.resize(806, 628)
        font = QtGui.QFont()
        font.setPointSize(10)
        ProjectInfoDialog.setFont(font)
        ProjectInfoDialog.setModal(True)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(ProjectInfoDialog)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.tabWidget = QtWidgets.QTabWidget(ProjectInfoDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 8, 1, 1, 1)
        self.txt_project_info = QtWidgets.QTextEdit(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.txt_project_info.sizePolicy().hasHeightForWidth()
        )
        self.txt_project_info.setSizePolicy(sizePolicy)
        self.txt_project_info.setObjectName("txt_project_info")
        self.gridLayout.addWidget(self.txt_project_info, 3, 0, 1, 2)
        self.txt_license_url = QtWidgets.QLineEdit(self.tab_2)
        self.txt_license_url.setObjectName("txt_license_url")
        self.gridLayout.addWidget(self.txt_license_url, 9, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_9 = QtWidgets.QLabel(self.tab_2)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_7.addWidget(self.label_9)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_7.addItem(spacerItem)
        self.btn_add_server = QtWidgets.QToolButton(self.tab_2)
        self.btn_add_server.setObjectName("btn_add_server")
        self.horizontalLayout_7.addWidget(self.btn_add_server)
        self.btn_remove_server = QtWidgets.QToolButton(self.tab_2)
        self.btn_remove_server.setObjectName("btn_remove_server")
        self.horizontalLayout_7.addWidget(self.btn_remove_server)
        self.gridLayout.addLayout(self.horizontalLayout_7, 11, 0, 1, 2)
        self.txt_contact_name = QtWidgets.QLineEdit(self.tab_2)
        self.txt_contact_name.setObjectName("txt_contact_name")
        self.gridLayout.addWidget(self.txt_contact_name, 7, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.txt_project_version = QtWidgets.QLineEdit(self.tab_2)
        self.txt_project_version.setObjectName("txt_project_version")
        self.gridLayout.addWidget(self.txt_project_version, 1, 1, 1, 1)
        self.txt_tos_url = QtWidgets.QLineEdit(self.tab_2)
        self.txt_tos_url.setObjectName("txt_tos_url")
        self.gridLayout.addWidget(self.txt_tos_url, 5, 0, 1, 2)
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 8, 0, 1, 1)
        self.txt_license_name = QtWidgets.QLineEdit(self.tab_2)
        self.txt_license_name.setObjectName("txt_license_name")
        self.gridLayout.addWidget(self.txt_license_name, 9, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 6, 1, 1, 1)
        self.lst_servers = QtWidgets.QListWidget(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lst_servers.sizePolicy().hasHeightForWidth())
        self.lst_servers.setSizePolicy(sizePolicy)
        self.lst_servers.setMaximumSize(QtCore.QSize(16777215, 80))
        self.lst_servers.setObjectName("lst_servers")
        self.gridLayout.addWidget(self.lst_servers, 14, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.txt_project_title = QtWidgets.QLineEdit(self.tab_2)
        self.txt_project_title.setObjectName("txt_project_title")
        self.gridLayout.addWidget(self.txt_project_title, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.txt_contact_email = QtWidgets.QLineEdit(self.tab_2)
        self.txt_contact_email.setObjectName("txt_contact_email")
        self.gridLayout.addWidget(self.txt_contact_email, 7, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_10 = QtWidgets.QLabel(self.tab_3)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.lst_common_headers = QtWidgets.QListWidget(self.tab_3)
        self.lst_common_headers.setObjectName("lst_common_headers")
        self.verticalLayout.addWidget(self.lst_common_headers)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lst_project_tags = QtWidgets.QListWidget(self.tab_5)
        self.lst_project_tags.setObjectName("lst_project_tags")
        self.horizontalLayout_5.addWidget(self.lst_project_tags)
        self.tabWidget.addTab(self.tab_5, "")
        self.horizontalLayout_6.addWidget(self.tabWidget)

        self.retranslateUi(ProjectInfoDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ProjectInfoDialog)

    def retranslateUi(self, ProjectInfoDialog):
        _translate = QtCore.QCoreApplication.translate
        ProjectInfoDialog.setWindowTitle(_translate("ProjectInfoDialog", "Project"))
        self.label_8.setText(_translate("ProjectInfoDialog", "License Name"))
        self.label_9.setText(_translate("ProjectInfoDialog", "Servers"))
        self.btn_add_server.setText(_translate("ProjectInfoDialog", "++"))
        self.btn_remove_server.setText(_translate("ProjectInfoDialog", "-"))
        self.label_5.setText(_translate("ProjectInfoDialog", "Contact Name"))
        self.label.setText(_translate("ProjectInfoDialog", "Title"))
        self.label_3.setText(_translate("ProjectInfoDialog", "Description"))
        self.label_7.setText(_translate("ProjectInfoDialog", "License URL"))
        self.label_6.setText(_translate("ProjectInfoDialog", "Contact Email"))
        self.label_2.setText(_translate("ProjectInfoDialog", "Version"))
        self.label_4.setText(_translate("ProjectInfoDialog", "Terms of Service URL"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2),
            _translate("ProjectInfoDialog", "General"),
        )
        self.label_10.setText(
            _translate(
                "ProjectInfoDialog",
                "Common Headers (Will be added to all API requests)",
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_3), _translate("ProjectInfoDialog", "Setup")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_5), _translate("ProjectInfoDialog", "Tags")
        )
