import logging

from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel

sdk_language_options = {
    'java': {

    }
}


class OpenApiSdkGeneratorPresenter:
    def __init__(self, view, parent=None):
        self.view = view
        self.main_window = parent

        # ui events
        self.view.lst_sdk_languages.currentItemChanged.connect(self.on_sdk_language_selected)
        self.view.btn_sdk_download.pressed.connect(self.on_download_sdk)

        # app events

    def on_download_sdk(self):
        print("Downloading SDK")
        print("Number of Arguments: {}".format(self.view.frame_options_layout.count()))
        for argument_widget in self.get_argument_widgets():
            print("{}-{}".format(argument_widget.objectName(), argument_widget.text()))
        # Prepare http request to create new sdk
        # Download SDK zip file in a temporary directory

    def get_argument_widgets(self):
        argument_widgets = []

        for i in range(self.view.frame_options_layout.count()):
            child_item = self.view.frame_options_layout.itemAt(i)
            if type(child_item.widget()) is QFrame:
                child_frame = child_item.widget()
                for child_frame_child in child_frame.children():
                    if type(child_frame_child) not in [QHBoxLayout, QLabel]:
                        argument_widgets.append(child_frame_child)

        return argument_widgets

    def on_sdk_language_selected(self, newly_selected_item, previous_selected_item):
        if not newly_selected_item:
            return

        newly_selected_environment = newly_selected_item.text()
        logging.debug(f"on_item_selection_changed: {newly_selected_environment}")
        self.view.render_argument()

    def show_dialog(self):
        # initiate dialog state
        self.view.show()
