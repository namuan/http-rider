from httprider.core.generators import utility_func_map


class UtilityFunctionsPresenter:
    def __init__(self, view, parent):
        self.view = view
        self.parent = parent

        # update list of functions
        for f in utility_func_map.keys():
            self.view.function_selector.addItem(f)

            # Event handlers to refresh generated values
        self.view.function_selector.currentIndexChanged[str].connect(
            self.transform_selected_text
        )

    def init(self):
        whole_text = self.parent.text()
        selected_text = self.parent.selected_text
        self.view.lbl_selected_text.setText(
            selected_text or whole_text or "Select some text"
        )
        self.transform_selected_text()

    def apply_transformation(self, selected_text, func_name):
        try:
            return utility_func_map.get(func_name)(selected_text)
        except Exception as e:
            return "Error: {}".format(e)

    def transform_selected_text(self):
        selected_text = self.view.lbl_selected_text.text()
        func_name = self.view.function_selector.currentText()
        self.view.lbl_transformed_text.setText(
            self.apply_transformation(selected_text, func_name)
        )

    def get_function(self):
        selected_text = self.view.lbl_selected_text.text()
        func_name = self.view.function_selector.currentText()
        return f'${{utils("{func_name}", "{selected_text}")}}'
