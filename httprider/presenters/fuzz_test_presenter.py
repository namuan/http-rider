import json

from mistune import markdown

from httprider.core import (
    get_variable_tokens,
    replace_variables,
    combine_request_headers,
)
from httprider.core import styles_from_file
from httprider.core.core_settings import app_settings
from httprider.core.http_statuses import *
from httprider.core.json_data_generator import jdg
from httprider.core.json_schema import schema_from_json
from httprider.core.safe_rest_api_interactor import rest_api_interactor, ApiWorkerData
from httprider.model.app_data import (
    ApiCall,
    ExchangeRequest,
    HttpExchange,
    ExchangeRequestType,
    ExchangeResponse,
)
from httprider.presenters.common import markdown_request, markdown_response


class FuzzTestPresenter:
    def __init__(self, view, parent=None):
        self.view = view
        self.main_window = parent
        self.selected_api: ApiCall = None
        self.pyg_styles = styles_from_file(":/themes/pyg.css")
        self.view.txt_fuzz_output.document().setDefaultStyleSheet(self.pyg_styles)
        self.__clear_results()

        # ui events
        self.view.btn_fuzz_test.clicked.connect(self.on_fuzz_test)

        # domain events
        app_settings.app_data_reader.signals.api_call_change_selection.connect(
            self.__on_updated_selected_api
        )

    def show_dialog(self):
        lbl = "{} {}".format(self.selected_api.http_method, self.selected_api.http_url)
        self.view.lbl_api_call.setText(lbl)
        self.__clear_results()
        self.view.show()

    def on_fuzz_test(self):
        request_counter = self.view.int_fuzz_count.value()
        max_array_items = self.view.int_max_array_items.value()
        max_string_length = self.view.int_max_string_length.value()
        jdg.update_limits(string_ml=max_string_length, array_ml=max_array_items)

        self.__clear_results()
        for _ in range(request_counter):
            exchange = self.__prepare_fuzzed_exchange_from_api_call(self.selected_api)
            api_worker_data = ApiWorkerData(
                exchange=exchange,
                on_success=self.__on_result,
                on_failure=self.__on_result,
            )
            rest_api_interactor.queue_worker_task(api_worker_data)

    def __clear_results(self):
        self.results_2xx = 0
        self.results_3xx = 0
        self.results_4xx = 0
        self.results_5xx = 0
        self.view.txt_fuzz_output.clear()
        self.__display_results()

    def __output_generator(self, exchange: HttpExchange):
        request_rendered = markdown_request(exchange)
        response_rendered = markdown_response(exchange)

        content = f"""### Request
{request_rendered}
### Response
{response_rendered}
=======================================================================================
        """
        return content

    def __update_results(self, exchange_response: ExchangeResponse):
        if is_2xx(exchange_response.http_status_code):
            self.results_2xx += 1
        elif is_3xx(exchange_response.http_status_code):
            self.results_3xx += 1
        elif is_4xx(exchange_response.http_status_code):
            self.results_4xx += 1
        elif is_5xx(exchange_response.http_status_code):
            self.results_5xx += 1

        self.__display_results()

    def __display_results(self):
        output = "2XX: {}, 3XX: {}, 4XX: {}, 5XX: {}".format(
            self.results_2xx, self.results_3xx, self.results_4xx, self.results_5xx
        )
        self.view.lbl_fuzz_results.setText(output)

    def __on_result(self, exchange: HttpExchange):
        md = self.__output_generator(exchange)
        self.view.txt_fuzz_output.appendHtml(markdown(md))
        self.__update_results(exchange.response)

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
        if not request_json_body:
            return ""
        request_schema = schema_from_json(request_json_body)
        return json.dumps(jdg.json_from_schema(request_schema.get("schema")))

    def __on_updated_selected_api(self, api_call):
        self.selected_api = api_call
