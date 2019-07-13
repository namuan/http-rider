from pygments import highlight
from pygments.lexers import data
from pygments.formatters.html import HtmlFormatter

from ..core import format_json
from ..model.app_data import ExchangeRequest, ExchangeResponse, ApiCall


def api_request_body_highlighted(api_call: ApiCall):
    return highlight(format_json(api_call.http_request_body), data.JsonLexer(), HtmlFormatter())


def request_body_highlighted(http_request: ExchangeRequest):
    return highlight(format_json(http_request.request_body), data.JsonLexer(), HtmlFormatter())


def response_body_highlighted(http_response: ExchangeResponse):
    return highlight(format_json(http_response.response_body), data.JsonLexer(), HtmlFormatter())
