from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import data

from ..core import format_json
from ..model.app_data import ExchangeRequest, ExchangeResponse, ApiCall


def highlight_format_json(plain_text):
    return highlight(format_json(plain_text), data.JsonLexer(), HtmlFormatter())


def api_request_body_highlighted(api_call: ApiCall):
    return highlight_format_json(api_call.http_request_body)


def request_body_highlighted(http_request: ExchangeRequest):
    return highlight_format_json(http_request.request_body)


def response_body_highlighted(http_response: ExchangeResponse):
    return highlight_format_json(http_response.response_body)
