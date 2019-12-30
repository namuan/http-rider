from httprider.core.api_call_interactor import api_call_interactor
from httprider.core.app_state_interactor import AppStateInteractor
from httprider.model.app_data import ApiCall


class EmptyFramePresenter:
    def __init__(self, parent_view):
        self.view = parent_view
        self.app_state_interactor = AppStateInteractor()
        self.view.btn_add_request.pressed.connect(self.on_btn_add_request)

    def on_btn_add_request(self):
        api_call = ApiCall()
        api_call.http_url = "https://httpbin.org/get"
        api_call.http_method = "GET"
        api_call.title = "Get httpbin"
        api_call.description = "Httpbin call to get request data"
        api_call.sequence_number = self.app_state_interactor.update_sequence_number()

        api_call_interactor.add_api_call(api_call)

        self.focus_http_url()

    def on_btn_add_separator(self):
        api_call = ApiCall()
        api_call.title = "Separator"
        api_call.is_separator = True
        api_call.sequence_number = self.app_state_interactor.update_sequence_number()
        api_call_interactor.add_api_call(api_call)

    def focus_http_url(self):
        self.__select_text(self.view.txt_http_url)

    def focus_headers(self):
        self.view.tabWidget.setCurrentIndex(1)

    def focus_query_params(self):
        self.view.tabWidget.setCurrentIndex(2)

    def focus_form_params(self):
        self.view.tabWidget.setCurrentIndex(3)

    def focus_request_body(self):
        self.view.tabWidget.setCurrentIndex(4)

    def focus_mocked_response(self):
        self.view.tabWidget.setCurrentIndex(5)

    def focus_http_method(self):
        self.view.cmb_http_method.setFocus(True)
        self.view.cmb_http_method.showPopup()

    def focus_description(self):
        self.view.tabWidget.setCurrentIndex(0)
        self.__select_text(self.view.txt_api_title)

    def __select_text(self, txt_field):
        txt_field.setFocus(True)
        txt_field.selectAll()

    def display(self):
        """Called when all API calls are removed from list"""
        self.view.empty_frame.show()
