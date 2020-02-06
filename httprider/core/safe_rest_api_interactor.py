import logging
from queue import Queue, Empty

import attr
from typing import Any

from httprider.core.core_settings import app_settings
from httprider.core import random_environment, combine_request_headers
from httprider.core.api_call_interactor import api_call_interactor
from httprider.external.rest_api_connector import (
    RestApiConnector,
    http_exchange_signals,
)
from httprider.model.app_data import (
    ApiCall,
    ExchangeRequest,
    HttpExchange,
    ExchangeResponse,
)


@attr.s(auto_attribs=True)
class ApiWorkerData(object):
    exchange: HttpExchange
    on_success: Any
    on_failure: Any


class SafeRestApiInteractor:
    """
    Singleton class
    [x] Should manages requests and invoking new RestApiConnector
    [x] Should queues requests and sequentially call RestApiConnector
    [x] Should provide callback hooks on success and failure for caller
    """

    worker_queue: Queue = Queue()
    api_workers = []
    any_worker_running: bool = False

    def __init__(self, app_config=app_settings):
        self.app_config = app_config

        # domain events
        http_exchange_signals.request_finished.connect(self.__request_finished)
        http_exchange_signals.fuzzed_request_finished.connect(self.__request_finished)
        http_exchange_signals.interrupt.connect(self.__on_halt_processing)

    def make_http_call(self, api_call: ApiCall):
        exchange_request = ExchangeRequest.from_api_call(api_call, hide_secrets=False)
        exchange_request.headers = combine_request_headers(
            self.app_config, exchange_request
        )
        exchange = HttpExchange(api_call_id=api_call.id, request=exchange_request)

        if api_call.mocked_response.is_enabled:
            exchange.response = ExchangeResponse.from_mocked_response(
                api_call.mocked_response
            )

        api_worker_data = ApiWorkerData(
            exchange=exchange,
            on_success=self.__on_success,
            on_failure=self.__on_failure,
        )
        self.queue_worker_task(api_worker_data)

    def queue_worker_task(self, api_worker_data: ApiWorkerData):
        logging.warning(
            f"Queuing request for API: {api_worker_data.exchange.api_call_id}"
        )
        self.worker_queue.put(api_worker_data)
        self.__process_queue()
        logging.info(f"Queue Size: {self.worker_queue.qsize()}")

    def __request_finished(self, api_call_id):
        logging.info("Api Call: {} - Worker completed".format(api_call_id))
        self.any_worker_running = False
        self.__process_queue()

    def __process_queue(self):
        if self.any_worker_running:
            logging.info("Worker running. Will check again once it finished processing")
        elif not self.worker_queue.empty():
            wrapped_queued_exchange: ApiWorkerData = self.worker_queue.get()
            logging.info(
                f"Processing queued exchange: {wrapped_queued_exchange.exchange.api_call_id}"
            )
            self.__process_exchange(wrapped_queued_exchange)
        else:
            logging.debug("Nothing in the queue")

    def __process_exchange(self, api_worker_data: ApiWorkerData):
        busy_worker = RestApiConnector(name=random_environment())
        self.__bind_signals(busy_worker, api_worker_data)

        # @todo: Check where do we remove workers.
        # Can we then use this instead of any_worker_running flag
        # Why do we need to create a list of workers if we are only running one at a time
        self.api_workers.append(busy_worker)

        logging.info(f"Scheduling API Call {api_worker_data.exchange.api_call_id}")
        busy_worker.exchange = api_worker_data.exchange
        busy_worker.start()
        self.any_worker_running = True

    def __on_success(self, exchange: HttpExchange):
        logging.info(f"API Call: {exchange.api_call_id} - __on_success")
        api_call = self.app_config.app_data_cache.get_api_call(exchange.api_call_id)
        api_call.last_response_code = exchange.response.http_status_code

        api_call_interactor.update_api_call(api_call.id, api_call)

        self.app_config.app_data_writer.add_http_exchange(exchange)

    def __on_failure(self, exchange: HttpExchange):
        logging.error(f"API Call: {exchange.api_call_id} - __on_failure -> {exchange}")
        api_call = self.app_config.app_data_cache.get_api_call(exchange.api_call_id)
        api_call.last_response_code = exchange.response.http_status_code
        api_call.last_assertion_result = None
        api_call_interactor.update_api_call(api_call.id, api_call)

        self.app_config.app_data_writer.add_http_exchange(exchange)

    def __on_halt_processing(self):
        logging.info(f"Clearing queue - items waiting: {self.worker_queue.qsize()}")
        while not self.worker_queue.empty():
            try:
                self.worker_queue.get(block=False)
            except Empty:
                continue

            self.worker_queue.task_done()

    def __bind_signals(self, rest_api_connector, api_worker_data: ApiWorkerData):
        rest_api_connector.signals.result.connect(api_worker_data.on_success)
        rest_api_connector.signals.error.connect(api_worker_data.on_failure)


rest_api_interactor = SafeRestApiInteractor()
