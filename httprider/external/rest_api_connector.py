import logging

from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from requests import PreparedRequest
from requests.exceptions import ConnectionError as RequestsConnectionError
from urllib3.exceptions import NewConnectionError

from httprider.core.constants import (
    CONTENT_TYPE_HEADER_IN_EXCHANGE,
    ContentType,
    ExchangeResponseStatus,
)
from httprider.core.core_settings import app_settings
from httprider.core.generators import is_file_function
from httprider.external import open_form_file
from httprider.external.requester import Requester
from httprider.model.app_data import ExchangeRequest, ExchangeResponse, HttpExchange

from ..core import (
    get_variable_tokens,
    guess_content_type,
    replace_response_variables,
    replace_variables,
)


class HttpExchangeSignals(QObject):
    request_started = pyqtSignal(str, str)
    request_finished = pyqtSignal(str)
    fuzzed_request_started = pyqtSignal(str, str)
    fuzzed_request_finished = pyqtSignal(str)
    interrupt = pyqtSignal()


http_exchange_signals = HttpExchangeSignals()


class RestApiResponseSignals(QObject):
    result = pyqtSignal(HttpExchange)
    error = pyqtSignal(HttpExchange)


class FuzzedRestApiResponseSignals(QObject):
    result = pyqtSignal(HttpExchange)
    error = pyqtSignal(HttpExchange)


class RestApiConnector(QThread):
    def __init__(self, name, app_config=app_settings):
        super().__init__()
        self.app_config = app_config
        self.tname = name
        self.halt_processing = False
        self.signals = RestApiResponseSignals()
        http_exchange_signals.interrupt.connect(self.on_halt_processing)
        self._exchange = None
        self.requester = Requester()

    @property
    def exchange(self):
        return self._exchange

    @exchange.setter
    def exchange(self, value):
        self._exchange = value

    def on_halt_processing(self):
        self.halt_processing = True
        logging.info(f"Received interrupt signal on {self.exchange}")

    def update_request(
        self,
        current_exchange_request: ExchangeRequest,
        prepared_request: PreparedRequest,
    ):
        """Update exchange request with prepared request if available"""
        if prepared_request:
            current_exchange_request.full_encoded_url = prepared_request.url or current_exchange_request
            current_exchange_request.headers = dict(prepared_request.headers.items())
            current_exchange_request.request_body = prepared_request.body or ""
            current_exchange_request.http_method = prepared_request.method
        else:
            current_exchange_request.full_encoded_url = current_exchange_request.http_url
        return current_exchange_request

    def convert_response(self, raw_response):
        res = ExchangeResponse(http_status_code=raw_response.status_code, response_body=raw_response.text)

        if res.response_body:
            res.response_body_type = guess_content_type(res.response_body)

        res.elapsed_time = raw_response.elapsed
        res.headers = raw_response.headers
        return res

    def mock_exchange(self, var_tokens):
        logging.info(f"<== Returning mocked Response ({self.exchange.api_call_id})")
        self.exchange.request.full_encoded_url = self.exchange.request.url_with_qp()
        self.exchange.response = replace_response_variables(var_tokens, self.exchange.response)
        self.exchange.response_status = ExchangeResponseStatus.PASSED

    def make_http_call(self):
        # preparing request with variable substitutions
        var_tokens = get_variable_tokens(self.app_config)
        self.exchange.request = replace_variables(var_tokens, self.exchange.request)

        # deriving request content type
        req: ExchangeRequest = self.exchange.request
        logging.info(
            f"==>[{self.tname}] make_http_call({self.exchange.api_call_id}): Http {req.http_method} to {req.http_url}"
        )

        # converting request to k/v structure
        kwargs = dict(headers=req.headers, params=req.query_params)

        content_type = req.headers.get(f"{CONTENT_TYPE_HEADER_IN_EXCHANGE}", ContentType.NONE.value)

        if req.request_body:
            req.request_body_type = guess_content_type(req.request_body)
            content_type = req.headers.get(CONTENT_TYPE_HEADER_IN_EXCHANGE, req.request_body_type.value)

        if req.form_params and "application/x-www-form-urlencoded" in content_type:
            req.request_body_type = ContentType.FORM
            kwargs["data"] = req.form_params
        elif req.form_params:
            if content_type:
                del kwargs["headers"][CONTENT_TYPE_HEADER_IN_EXCHANGE]

            kwargs["files"] = {
                k: open_form_file(is_file_function(v).group(2))
                for k, v in req.form_params.items()
                if is_file_function(v)
            }
        elif req.request_body:
            kwargs["data"] = req.request_body

        # Signal API call started
        progress_message = f"{req.http_method} call to {req.http_url}"
        if req.is_fuzzed():
            http_exchange_signals.fuzzed_request_started.emit(progress_message, self.exchange.api_call_id)
        else:
            http_exchange_signals.request_started.emit(progress_message, self.exchange.api_call_id)

        if self.exchange.response.is_mocked:
            self.mock_exchange(var_tokens)
        else:
            response, err = self.requester.make_request(req.http_method, req.http_url, kwargs)
            self.exchange.request = self.update_request(self.exchange.request, response.request)

            # Building exchange response
            if err and isinstance(err, RequestsConnectionError):
                nce: NewConnectionError = err.args[0].reason
                error_response = ExchangeResponse(http_status_code=-1, response_body=str(nce.args[0]))
                self.exchange.response = error_response
                self.exchange.failed()
            elif err:
                error_response = ExchangeResponse(http_status_code=-1, response_body=str(err))
                self.exchange.response = error_response
                self.exchange.failed()
            else:
                self.exchange.response = self.convert_response(response)
                self.exchange.passed()

            logging.info(
                f"<== make_http_call({self.exchange.api_call_id}): "
                f"Received response in {self.exchange.response.elapsed_time}"
            )

            # Cleanup (for both success/failure)
            for _fk, fv in kwargs.get("files", {}).items():
                fv.close()

            # This is to make sure that we cleanly quit this thread
            if self.halt_processing:
                self.halt_processing = False
                http_exchange_signals.request_finished.emit()
                http_exchange_signals.fuzzed_request_finished.emit()
                return

        if self.exchange.is_passed():
            self.signals.result.emit(self.exchange)
        else:
            self.signals.error.emit(self.exchange)

        if req.is_fuzzed():
            http_exchange_signals.fuzzed_request_finished.emit(self.exchange.api_call_id)
        else:
            http_exchange_signals.request_finished.emit(self.exchange.api_call_id)

    @pyqtSlot()
    def run(self):
        logging.info(f"Running Rest API Connector for API: {self.exchange.api_call_id}")
        try:
            self.make_http_call()
        except Exception as e:
            http_exchange_signals.request_finished.emit(self.exchange.api_call_id)
            logging.exception(f"Unhandled exception: {e}")
            raise
