from httprider.core.generators import utility_func_map


class UtilityFunctionsPresenter:
    def __init__(self, view, parent):
        self.view = view
        self.parent = parent

        # update list of functions
        for f in utility_func_map:
            self.view.function_selector.addItem(f)

        self.view.btn_copy_transformed.clicked.connect(self.on_copy_clipboard)

    def init(self):
        whole_text = self.parent.text()
        selected_text = self.parent.selected_text
        self.view.lbl_selected_text.setText(selected_text or whole_text or "Select some text")
        self.transform_selected_text()

    def apply_transformation(self, selected_text, func_name):
        try:
            return utility_func_map.get(func_name)(selected_text)
        except Exception as e:
            return f"Error: {e}"

    def on_copy_clipboard(self):
        self.view.txt_transformed_text.selectAll()
        self.view.txt_transformed_text.copy()

    def transform_selected_text(self):
        selected_text = self.view.lbl_selected_text.text()
        func_name = self.view.function_selector.currentText()
        self.view.txt_transformed_text.setPlainText(self.apply_transformation(selected_text, func_name))

    def get_function(self):
        selected_text = self.view.lbl_selected_text.text()
        func_name = self.view.function_selector.currentText()
        return f'${{utils("{func_name}", "{selected_text}")}}'
