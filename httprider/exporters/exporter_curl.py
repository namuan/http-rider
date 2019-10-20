import attr
from pygments.lexers.shell import BashLexer
from typing import List

from ..core.core_settings import app_settings
from ..exporters import *
from ..model.app_data import ApiCall, HttpExchange


def to_curl(api_call: ApiCall, exchange: HttpExchange, compressed=False, verify=True):
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

    if req_qp:
        http_url = http_url + "?" + "&".join([f"{k}={v}" for k, v in req_qp.items()])

    parts = [
        ('curl', None),
        ('-X', http_method),
    ]

    for k, v in sorted(req_headers.items()):
        parts += [('-H', '{0}: {1}'.format(k, v))]

    if req_body:
        body = req_body
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        parts += [('-d', body)]

    if compressed:
        parts += [('--compressed', None)]

    if not verify:
        parts += [('--insecure', None)]

    parts += [(None, http_url)]

    flat_parts = []
    for k, v in parts:
        if k:
            flat_parts.append(k)
        if v:
            flat_parts.append("'{0}'".format(v))

    return ' '.join(flat_parts)


@attr.s
class CurlExporter:
    name: str = "Curl"
    output_ext: str = "sh"

    def export_data(self, api_calls: List[ApiCall]):
        output = [
            self.__export_api_call(api_call)
            for api_call in api_calls
        ]
        return "<br/>".join(output)

    def __export_api_call(self, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        doc = f"""# {api_call.title}
# 
{to_curl(api_call, last_exchange)}
"""
        return highlight(doc, BashLexer(), HtmlFormatter())


exporter = CurlExporter()
