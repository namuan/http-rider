class UtilityFunctionsPresenter:
    def __init__(self, view, parent):
        self.view = view
        self.parent = parent

        # Event handlers to refresh generated values
        self.view.function_selector.currentIndexChanged[str].connect(self.transform_selected_text)

    def init(self):
        whole_text = self.parent.text()
        selected_text = self.parent.selected_text
        self.view.lbl_selected_text.setText(selected_text or whole_text)
        self.transform_selected_text()

    def apply_transformation(self, selected_text, func_name):
        return f"{func_name}(\"{selected_text}\")"

    def transform_selected_text(self):
        selected_text = self.view.lbl_selected_text.text()
        func_name = self.view.function_selector.currentText()
        self.view.lbl_transformed_text.setText(
            self.apply_transformation(selected_text, func_name)
        )

    def get_function(self):
        selected_text = self.view.lbl_selected_text.text()
        func_name = self.view.function_selector.currentText()
        return self.apply_transformation(selected_text, func_name)
