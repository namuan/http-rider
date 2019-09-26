import attr
from pygments.lexers.shell import BashLexer
from typing import List

from ..core.core_settings import app_settings
from ..exporters import *
from ..model.app_data import ApiCall, HttpExchange


def to_slow_cooker(api_call: ApiCall, exchange: HttpExchange, compressed=False, verify=True):
    http_method = api_call.http_method
    http_url = api_call.http_url
    req_headers = {k: v.value for k, v in api_call.http_headers.items()}
    req_qp = {k: v.value for k, v in api_call.http_params.items()}
    req_body = api_call.http_request_body

    if exchange.response.http_status_code != 0:
        http_method = exchange.request.http_method
        http_url = exchange.request.http_url
        req_qp = exchange.request.query_params
        req_headers = exchange.request.headers
        req_body = exchange.request.request_body

    if req_qp:
        http_url = http_url + "?" + "&".join([f"{k}={v}" for k, v in req_qp.items()])

    parts = [
        ('slow_cooker', None),
        ('-method', http_method),
        ('-qps 100', None),
        ('-concurrency 10', None)
    ]

    for k, v in sorted(req_headers.items()):
        parts += [('-header', '{0}: {1}'.format(k, v))]

    if req_body:
        body = req_body
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        parts += [('-data', body)]

    parts += [(None, http_url)]

    flat_parts = []
    for k, v in parts:
        if k:
            flat_parts.append(k)
        if v:
            flat_parts.append("'{0}'".format(v))

    return ' '.join(flat_parts)


@attr.s
class SlowCookerExporter:
    name: str = "Slow Cooker (Performance)"
    output_ext: str = "sh"

    def export_data(self, api_calls: List[ApiCall]):
        header = """
## Download and setup slow_cooker from https://github.com/buoyantio/slow_cooker<br/>
## Brief description about the parameters used<br/>
## -qps: QPS to send to backends per request thread<br/>
## -concurrency: Number of goroutines to run, each at the specified QPS level. Measure total QPS as qps * concurrency<br/>
## -iterations: Number of iterations for the experiment. Exits gracefully after iterations * interval (default 0, meaning infinite)<br/>
## -header: Adds additional headers to each request. Can be specified multiple times. Format is key: value<br/>
## -interval: How often to report stats to stdout<br/>
## -method: Determines which HTTP method to use when making the request<br/>
        """
        output = [
            self.__export_api_call(api_call)
            for api_call in api_calls
        ]
        return header + "<br/>".join(output)

    def __export_api_call(self, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        doc = f"""# {api_call.title}
# 
{to_slow_cooker(api_call, last_exchange)}
"""
        return highlight(doc, BashLexer(), HtmlFormatter())


exporter = SlowCookerExporter()
