from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import data

from ..core import format_json
from ..model.app_data import ExchangeRequest, ExchangeResponse, ApiCall


def highlight_format_json(plain_text, formatter=HtmlFormatter()):
    return highlight(format_json(plain_text), data.JsonLexer(), formatter)


def api_request_body_highlighted(api_call: ApiCall):
    return highlight_format_json(api_call.http_request_body)


def request_body_highlighted(http_request: ExchangeRequest):
    return highlight_format_json(http_request.request_body)


def response_body_highlighted(http_response: ExchangeResponse):
    return highlight_format_json(http_response.response_body)


from . import exporter_apickli
from . import exporter_curl
from . import exporter_markdown
from . import exporter_mermaid
from . import exporter_openapi_v3
from . import exporter_postman_dump
from . import exporter_restassured

exporter_plugins = {
    'apickli': exporter_apickli,
    'curl': exporter_curl,
    'markdown': exporter_markdown,
    'mermaid': exporter_mermaid,
    'openapi_v3': exporter_openapi_v3,
    'postman_dump': exporter_postman_dump,
    'restassured': exporter_restassured
}
