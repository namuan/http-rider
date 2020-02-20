from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog

from httprider.generated.openapi_sdk_gen_dialog import Ui_OpenApiSdkDialog
from httprider.presenters import OpenApiSdkGeneratorPresenter


class OpenApiGeneratorDialog(QDialog, Ui_OpenApiSdkDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.presenter = OpenApiSdkGeneratorPresenter(self, parent)

    def show_dialog(self):
        self.presenter.show_dialog()

    def render_argument(self):
        frame_argument = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        frame_argument.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame_argument.setFrameShadow(QtWidgets.QFrame.Raised)
        frame_argument.setObjectName("frame_argument")

        frame_argument_layout = QtWidgets.QHBoxLayout(frame_argument)
        frame_argument_layout.setObjectName("argument_layout_1")

        arg_project_name = QtWidgets.QLabel(frame_argument)
        arg_project_name.setObjectName("lbl_arg_project_name")
        arg_project_name.setText("Project Name")
        frame_argument_layout.addWidget(arg_project_name)

        arg_project_name = QtWidgets.QLineEdit(frame_argument)
        arg_project_name.setObjectName("txt_arg_project_name")
        frame_argument_layout.addWidget(arg_project_name)

        self.frame_options_layout.addWidget(frame_argument)
