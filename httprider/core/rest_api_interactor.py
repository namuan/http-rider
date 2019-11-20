import logging
from queue import Queue, Empty

from .core_settings import app_settings
from ..core import random_environment, combine_request_headers
from ..core.api_call_interactor import api_call_interactor
from ..external.rest_api_connector import RestApiConnector, http_exchange_signals
from ..model.app_data import ApiCall, ExchangeRequest, HttpExchange, ExchangeResponse


class RestApiInteractor:
    worker_queue: Queue = Queue()
    api_workers = []
    api_worker = RestApiConnector(name=random_environment())

    def __init__(self):
        self.bind_signals()

        http_exchange_signals.request_finished.connect(self.process_queue)
        http_exchange_signals.interrupt.connect(self.on_halt_processing)

    def on_halt_processing(self):
        logging.info(f"Terminating thread: {self.api_worker.tname}")
        self.api_worker = RestApiConnector(name=random_environment())
        self.bind_signals()

        logging.info(f"Clearing queue - items waiting: {self.worker_queue.qsize()}")
        while not self.worker_queue.empty():
            try:
                self.worker_queue.get(block=False)
            except Empty:
                continue

            self.worker_queue.task_done()

    def bind_signals(self):
        self.api_worker.signals.result.connect(self.__on_success)
        self.api_worker.signals.error.connect(self.__on_failure)

    def process_queue(self):
        logging.info(f"Status of API Worker: {self.api_worker.isRunning()}")
        if not self.worker_queue.empty():
            self.api_worker = RestApiConnector(name=random_environment())
            self.bind_signals()

            queued_exchange = self.worker_queue.get()
            logging.info(f"Processing queued exchange: {queued_exchange.api_call_id}")
            self.process_exchange(queued_exchange)
        else:
            logging.debug("Nothing in the queue")

    def make_http_call(self, api_call: ApiCall):
        exchange_request = ExchangeRequest.from_api_call(api_call)
        exchange_request.headers = combine_request_headers(
            app_settings, exchange_request
        )
        exchange = HttpExchange(api_call_id=api_call.id, request=exchange_request)

        if api_call.mocked_response.is_enabled:
            exchange.response = ExchangeResponse.from_mocked_response(
                api_call.mocked_response
            )

        if self.api_worker.isRunning():
            running_exchange: HttpExchange = self.api_worker.exchange
            logging.warning(
                f"Worker is running for API: {running_exchange.api_call_id}"
            )
            logging.warning(f"Should queue request for API: {exchange.api_call_id}")
            self.worker_queue.put(exchange)
        else:
            self.process_exchange(exchange)

        logging.info(f"Queue Size: {self.worker_queue.qsize()}")

    def process_exchange(self, exchange: HttpExchange):
        self.api_workers.append(self.api_worker)
        logging.info(f"Scheduling API Call {exchange.api_call_id}")
        self.api_worker.exchange = exchange
        self.api_worker.start()

    def __on_success(self, exchange: HttpExchange):
        logging.info(f"API Call: {exchange.api_call_id} - __on_success")
        api_call = app_settings.app_data_cache.get_api_call(exchange.api_call_id)
        api_call.last_response_code = exchange.response.http_status_code

        api_call_interactor.update_api_call(api_call.id, api_call)

        app_settings.app_data_writer.add_http_exchange(exchange)

    def __on_failure(self, exchange: HttpExchange):
        logging.error(f"API Call: {exchange.api_call_id} - __on_failure -> {exchange}")
        api_call = app_settings.app_data_cache.get_api_call(exchange.api_call_id)
        api_call.last_response_code = exchange.response.http_status_code
        api_call.last_assertion_result = None
        api_call_interactor.update_api_call(api_call.id, api_call)

        app_settings.app_data_writer.add_http_exchange(exchange)


rest_api_interactor = RestApiInteractor()
