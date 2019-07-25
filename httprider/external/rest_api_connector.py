import logging
import time

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from requests.exceptions import ConnectionError
from urllib3.exceptions import NewConnectionError

from ..core import guess_content_type, replace_variables, replace_response_variables, get_variable_tokens
from ..core.constants import ContentType
from ..core.core_settings import app_settings
from ..core.generators import is_file_function
from ..external import open_form_file
from ..external.requester import Requester
from ..model.app_data import ExchangeRequest, ExchangeResponse, HttpExchange


class HttpExchangeSignals(QObject):
    request_started = pyqtSignal(str, str)
    request_finished = pyqtSignal()
    interrupt = pyqtSignal()


http_exchange_signals = HttpExchangeSignals()


class RestApiResponseSignals(QObject):
    result = pyqtSignal(HttpExchange)
    error = pyqtSignal(HttpExchange)


class RestApiConnector(QThread):

    def __init__(self, name):
        super(RestApiConnector, self).__init__()
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

    def convert_response(self, raw_response):
        res = ExchangeResponse(
            http_status_code=raw_response.status_code,
            response_body=raw_response.text
        )

        if res.response_body:
            res.response_body_type = guess_content_type(res.response_body)

        res.elapsed_time = raw_response.elapsed
        res.headers = raw_response.headers
        return res

    def make_http_call(self):
        var_tokens = get_variable_tokens(app_settings)
        self.exchange.request = replace_variables(var_tokens, self.exchange.request)
        req: ExchangeRequest = self.exchange.request
        logging.info(
            f"==>[{self.tname}] make_http_call({self.exchange.api_call_id}): Http {req.http_method} to {req.http_url}")
        kwargs = dict(
            headers=req.headers,
            params=req.query_params
        )

        content_type = ContentType.NONE.value

        if req.request_body:
            req.request_body_type = guess_content_type(req.request_body)
            content_type = req.headers.get('Content-Type', req.request_body_type.value)

        if req.form_params and 'application/x-www-form-urlencoded' in content_type:
            kwargs['data'] = req.form_params
        elif req.form_params:
            if content_type:
                del kwargs['headers']['Content-Type']

            kwargs['files'] = {
                k: open_form_file(is_file_function(v).group(2))
                for k, v in req.form_params.items()
                if is_file_function(v)
            }
        elif req.request_body:
            kwargs['data'] = req.request_body

        try:
            progress_message = f"{req.http_method} call to {req.http_url}"
            http_exchange_signals.request_started.emit(progress_message, self.exchange.api_call_id)

            if self.exchange.response.is_mocked:
                logging.info(f"<== Returning mocked Response ({self.exchange.api_call_id})")
                self.exchange.response = replace_response_variables(var_tokens, self.exchange.response)
            else:
                response = self.requester.make_request(req.http_method, req.http_url, kwargs)
                self.exchange.response = self.convert_response(response)

                for fk, fv in kwargs.get('files', {}).items():
                    fv.close()

                logging.info(
                    f"<== make_http_call({self.exchange.api_call_id}): "
                    f"Received response in {self.exchange.response.elapsed_time}"
                )

                # This is to make sure that we cleanly quit this thread
                if self.halt_processing:
                    self.halt_processing = False
                    http_exchange_signals.request_finished.emit()
                    return

            self.signals.result.emit(self.exchange)
        except ConnectionError as e:
            nce: NewConnectionError = e.args[0].reason
            error_response = ExchangeResponse(
                http_status_code=-1,
                response_body=nce.args[0]
            )
            self.exchange.response = error_response
            self.signals.error.emit(self.exchange)
        except Exception as e:
            logging.error(e)
            error_response = ExchangeResponse(
                http_status_code=-1,
                response_body=str(e)
            )
            self.exchange.response = error_response
            self.signals.error.emit(self.exchange)

        http_exchange_signals.request_finished.emit()

    @pyqtSlot()
    def run(self):
        logging.info(f"Running Rest API Connector for API: {self.exchange.api_call_id}")
        try:
            self.make_http_call()
            # NOTE: Giving main thread some time to write data
            # As we raised events in the scheduler thread
            # which are consumed by Main thread
            # Otherwise data is corrupted if we try to read/write at the same time
            # @todo: Re-design and remove the need to put in this sleep
            time.sleep(0.5)
        except Exception as e:
            logging.error(f"Unhandled exception: {e}")
            raise e
