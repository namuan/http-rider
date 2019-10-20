import re

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import data

from ..core import format_json
from ..model.app_data import ExchangeRequest, ExchangeResponse, ApiCall

internal_var_selector = re.compile(r'\$\{(\w+)\}')


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


def extract_uri(url, servers):
    matched_server = next((server for server in servers if url.startswith(server)), None)
    if matched_server:
        return url.replace(matched_server, "")

    return url


# Import statements after any function definitions as they are using
# from the exporters

from . import exporter_apickli
from . import exporter_curl
from . import exporter_markdown
from . import exporter_mermaid
from . import exporter_openapi_v3
from . import exporter_runscope
from . import exporter_restassured
from . import exporter_python_requests
from . import exporter_plantuml
from . import exporter_slow_cooker

exporter_plugins = {
    'runscope': exporter_runscope,
    'apickli': exporter_apickli,
    'slow_cooker': exporter_slow_cooker,
    'plant_uml': exporter_plantuml,
    'python_requests': exporter_python_requests,
    'curl': exporter_curl,
    'markdown': exporter_markdown,
    'mermaid': exporter_mermaid,
    'openapi_v3': exporter_openapi_v3,
    'restassured': exporter_restassured,
}
