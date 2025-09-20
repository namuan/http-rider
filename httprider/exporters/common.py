import re

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import data
from yapf.yapflib.yapf_api import FormatCode

from ..core import format_json
from ..model.app_data import ApiCall, ExchangeRequest, ExchangeResponse, HttpExchange

internal_var_selector = re.compile(r"\$\{(\w+)\}")


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
    rgx = r"[^a-zA-Z]"
    return re.sub(rgx, "", norm_title)


def dict_formatter(dict_items, form, splitter=","):
    return splitter.join([form.format(**locals()) for k, v in dict_items])


def extract_uri(url, servers):
    matched_server = next((server for server in servers if url.startswith(server)), None)
    if matched_server:
        return url.replace(matched_server, "")

    return url


def to_curl(api_call: ApiCall, exchange: HttpExchange, compressed=False, verify=True):
    if api_call:
        http_method = api_call.http_method
        http_url = api_call.http_url
        req_headers = api_call.enabled_headers()
        req_qp = api_call.enabled_query_params()
        req_body = api_call.request_body_without_comments()

    if exchange.response.http_status_code != 0:
        http_method = exchange.request.http_method
        http_url = exchange.request.http_url
        req_qp = exchange.request.query_params
        req_headers = exchange.request.headers
        req_body = exchange.request.request_body
    elif not api_call:
        raise ValueError(
            f"Unable to make curl request as api_call is null and exchange response is {exchange.response}"
        )

    if req_qp:
        http_url = http_url + "?" + "&".join([f"{k}={v}" for k, v in req_qp.items()])

    parts = [("curl", None), ("-X", http_method)]

    for k, v in sorted(req_headers.items()):
        parts += [("-H", f"{k}: {v}")]

    if req_body:
        body = req_body
        if isinstance(body, bytes):
            body = body.decode("utf-8")
        parts += [("-d", body)]

    if compressed:
        parts += [("--compressed", None)]

    if not verify:
        parts += [("--insecure", None)]

    parts += [(None, http_url)]

    flat_parts = []
    for k, v in parts:
        if k:
            flat_parts.append(k)
        if v:
            flat_parts.append(f"'{v}'")

    return " ".join(flat_parts)


def format_python_code(unformatted_code):
    return FormatCode(unformatted_code, style_config="pep8")
