import logging

from .core_settings import app_settings
from .worker_pool import single_worker
from ..external.rest_api_connector import RestApiConnector
from ..model.app_data import ApiCall, ExchangeRequest, HttpExchange


def make_http_call(api_call: ApiCall, on_success=None, on_failure=None):
    exchange_request = ExchangeRequest.from_api_call(api_call)

    # inject common headers respecting existing headers on the request
    project_info = app_settings.app_data_reader.get_or_create_project_info()
    common_headers = {k: v.display_text for k, v in project_info.common_headers.items()}
    exchange_request.headers = {**common_headers, **exchange_request.headers}

    exchange = HttpExchange(
        api_call_id=api_call.id,
        request=exchange_request
    )
    api_worker = RestApiConnector(exchange)
    api_worker.signals.result.connect(lambda ex: __on_success(ex, on_success))
    api_worker.signals.error.connect(lambda ex: __on_failure(ex, on_failure))
    single_worker.schedule(api_worker)


def __on_success(exchange: HttpExchange, parent_on_success):
    api_call = app_settings.app_data_reader.get_api_call(exchange.api_call_id)
    api_call.last_response_code = exchange.response.http_status_code
    app_settings.app_data_writer.update_api_call(api_call.id, api_call)
    new_exchange_id = app_settings.app_data_writer.add_http_exchange(exchange)
    exchange.id = new_exchange_id
    if parent_on_success:
        parent_on_success(exchange)


def __on_failure(exchange: HttpExchange, parent_on_failure):
    logging.error(f"Unable to get response: {exchange}")
    api_call = app_settings.app_data_reader.get_api_call(exchange.api_call_id)
    api_call.last_response_code = exchange.response.http_status_code
    app_settings.app_data_writer.update_api_call(api_call.id, api_call)
    new_exchange_id = app_settings.app_data_writer.add_http_exchange(exchange)
    exchange.id = new_exchange_id
    if parent_on_failure:
        parent_on_failure(exchange)
