class GeneratorsMenuPresenter:
    def __init__(self, parent):
        self.main_window = parent

    def on_openapi_sdk_generator(self):
        self.main_window.openapi_sdk_generator_dialog.show_dialog()
