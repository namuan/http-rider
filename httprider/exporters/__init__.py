import re

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import data

from ..core import format_json
from ..model.app_data import ExchangeRequest, ExchangeResponse, ApiCall


def highlight_format_json(plain_text, formatter=HtmlFormatter()):
    if not plain_text:
        return ""

    return highlight(format_json(plain_text), data.JsonLexer(), formatter)


def api_request_body_highlighted(api_call: ApiCall):
    return highlight_format_json(api_call.http_request_body)


def request_body_highlighted(http_request: ExchangeRequest):
    return highlight_format_json(http_request.request_body)


def response_body_highlighted(http_response: ExchangeResponse):
    return highlight_format_json(http_response.response_body)


def encode_json_string(json_string):
    return json_string.replace('"', '\\"')


def get_base_url(api_call: ApiCall):
    return api_call.http_url


def get_function_name(api_call: ApiCall):
    norm_title = api_call.title.lower().strip()
    rgx = r'[^a-zA-Z]'
    return re.sub(rgx, '', norm_title)


def dict_formatter(dict_items, form, splitter=","):
    return splitter.join([
        form.format(**locals())
        for k, v in dict_items
    ])


from . import exporter_apickli
from . import exporter_curl
from . import exporter_markdown
from . import exporter_mermaid
from . import exporter_openapi_v3
from . import exporter_postman_dump
from . import exporter_restassured
from . import exporter_python_requests

exporter_plugins = {
    'python_requests': exporter_python_requests,
    'apickli': exporter_apickli,
    'curl': exporter_curl,
    'markdown': exporter_markdown,
    'mermaid': exporter_mermaid,
    'openapi_v3': exporter_openapi_v3,
    'postman_dump': exporter_postman_dump,
    'restassured': exporter_restassured,
}
