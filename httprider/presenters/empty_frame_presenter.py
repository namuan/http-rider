from httprider.core.api_call_interactor import api_call_interactor
from httprider.core.app_state_interactor import AppStateInteractor
from ..core.core_settings import app_settings
from ..model.app_data import ApiCall


class EmptyFramePresenter:
    def __init__(self, parent_view):
        self.view = parent_view
        self.app_state_interactor = AppStateInteractor()
        self.view.btn_add_request.pressed.connect(self.on_btn_add_request)

    def on_btn_add_request(self):
        api_call = ApiCall()
        api_call.http_url = "http://127.0.0.1:8000/get"
        api_call.http_method = "GET"
        api_call.title = "Get httpbin"
        api_call.description = "Httpbin call to get request data"
        api_call.sequence_number = self.app_state_interactor.update_sequence_number()

        # Migration
        api_call_interactor.add_api_call(api_call)

        self.focus_http_url()

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

    def focus_http_method(self):
        self.view.cmb_http_method.setFocus(True)
        self.view.cmb_http_method.showPopup()

    def focus_description(self):
        self.view.tabWidget.setCurrentIndex(0)
        self.__select_text(self.view.txt_api_title)

    def __select_text(self, txt_field):
        txt_field.setFocus(True)
        txt_field_value = txt_field.text()
        txt_field.setSelection(0, len(txt_field_value))

    def display(self):
        """Called when all API calls are removed from list"""
        self.view.empty_frame.show()
