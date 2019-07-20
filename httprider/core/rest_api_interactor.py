import logging
from queue import Queue

from .core_settings import app_settings
from ..external.rest_api_connector import RestApiConnector, http_exchange_signals
from ..model.app_data import ApiCall, ExchangeRequest, HttpExchange


class RestApiInteractor:
    worker_queue: Queue = Queue()
    api_worker = RestApiConnector()

    def __init__(self):
        http_exchange_signals.request_finished.connect(self.process_queue)

    def process_queue(self):
        if not self.worker_queue.empty():
            queued_exchange = self.worker_queue.get()
            logging.info(f"Processing queued exchange: {queued_exchange.api_call_id}")
            self.process_exchange(queued_exchange, None, None)
        else:
            logging.debug("Nothing in the queue")

    def make_http_call(self, api_call: ApiCall, on_success=None, on_failure=None):
        exchange_request = ExchangeRequest.from_api_call(api_call)

        # inject common headers respecting existing headers on the request
        project_info = app_settings.app_data_reader.get_or_create_project_info()
        common_headers = {k: v.display_text for k, v in project_info.common_headers.items()}
        exchange_request.headers = {**common_headers, **exchange_request.headers}

        exchange = HttpExchange(
            api_call_id=api_call.id,
            request=exchange_request
        )

        if self.api_worker.isRunning():
            running_exchange: HttpExchange = self.api_worker.exchange
            logging.warning(f"Worker is running for API: {running_exchange.api_call_id}")
            logging.warning(f"Should queue request for API: {exchange.api_call_id}")
            self.worker_queue.put(exchange)
        else:
            self.process_exchange(exchange, on_success, on_failure)

        logging.info(f"Queue Size: {self.worker_queue.qsize()}")

    def process_exchange(self, exchange: HttpExchange, on_success, on_failure):
        logging.info(f"Scheduling API Call {exchange.api_call_id}")
        self.api_worker.exchange = exchange
        self.api_worker.signals.result.connect(lambda ex: self.__on_success(ex, on_success))
        self.api_worker.signals.error.connect(lambda ex: self.__on_failure(ex, on_failure))
        self.api_worker.start()

    def __on_success(self, exchange: HttpExchange, parent_on_success):
        api_call = app_settings.app_data_reader.get_api_call(exchange.api_call_id)
        api_call.last_response_code = exchange.response.http_status_code
        app_settings.app_data_writer.update_api_call(api_call.id, api_call)
        new_exchange_id = app_settings.app_data_writer.add_http_exchange(exchange)
        exchange.id = new_exchange_id
        if parent_on_success:
            parent_on_success(exchange)

    def __on_failure(self, exchange: HttpExchange, parent_on_failure):
        logging.error(f"Unable to get response: {exchange}")
        api_call = app_settings.app_data_reader.get_api_call(exchange.api_call_id)
        api_call.last_response_code = exchange.response.http_status_code
        api_call.last_assertion_result = None
        app_settings.app_data_writer.update_api_call(api_call.id, api_call)
        new_exchange_id = app_settings.app_data_writer.add_http_exchange(exchange)
        exchange.id = new_exchange_id
        if parent_on_failure:
            parent_on_failure(exchange)
