class OpenApiSdkGeneratorPresenter:
    def __init__(self, view, parent=None):
        self.view = view
        self.main_window = parent

        # ui events

        # app events

    def show_dialog(self):
        # initiate dialog state
        self.view.show()
