import json

from ..core.safe_rest_api_interactor import rest_api_interactor
from ..core import get_variable_tokens, replace_variables, combine_request_headers
from ..core.core_settings import app_settings
from ..core.json_schema import schema_from_json, json_from_schema
from ..model.app_data import ApiCall, ExchangeRequest, HttpExchange, ExchangeRequestType


class FuzzTestPresenter:
    def __init__(self, view, parent=None):
        self.view = view
        self.main_window = parent
        self.selected_api: ApiCall = None
        # ui events
        self.view.btn_fuzz_test.clicked.connect(self.on_fuzz_test)

        # domain events
        app_settings.app_data_reader.signals.api_call_change_selection.connect(
            self.__on_updated_selected_api
        )

    def on_fuzz_test(self):
        exchange = self.__prepare_fuzzed_exchange_from_api_call(self.selected_api)
        request_counter = self.view.txt_fuzz_count.value()
        for _ in range(request_counter):
            self.view.txt_fuzz_output.appendHtml(str(exchange))
            rest_api_interactor.queue_exchange(exchange)

    def show_dialog(self):
        lbl = "Generating fuzz data for {} {}".format(
            self.selected_api.http_method, self.selected_api.http_url
        )
        self.view.lbl_api_call.setText(lbl)
        self.view.txt_fuzz_output.clear()
        self.view.show()

    def __prepare_fuzzed_exchange_from_api_call(self, api_call: ApiCall):
        exchange_request: ExchangeRequest = self.__get_prepared_request(api_call)
        exchange_request.request_type = ExchangeRequestType.FUZZED
        exchange_request.request_body = self.__generate_fuzzed_payload(
            exchange_request.request_body
        )
        return HttpExchange(api_call_id=api_call.id, request=exchange_request)

    def __get_prepared_request(self, api_call: ApiCall):
        exchange_request = ExchangeRequest.from_api_call(api_call)
        exchange_request.headers = combine_request_headers(
            app_settings, exchange_request
        )
        var_tokens = get_variable_tokens(app_settings)
        exchange_request = replace_variables(var_tokens, exchange_request)

        return exchange_request

    def __generate_fuzzed_payload(self, request_json_body):
        request_schema = schema_from_json(request_json_body)
        return json.dumps(json_from_schema(request_schema.get("schema")))

    def __on_updated_selected_api(self, api_call):
        self.selected_api = api_call
