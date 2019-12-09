class SharePreviewPresenter:
    def __init__(self, view, parent=None):
        self.view = view
        self.main_window = parent

    def show_dialog(self):
        self.view.show()
