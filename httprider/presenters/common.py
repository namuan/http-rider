from pygments.formatters.other import NullFormatter

from httprider.core import elapsed_time_formatter
from httprider.exporters.common import dict_formatter, highlight_format_json
from httprider.model.app_data import HttpExchange


def markdown_request(exchange: HttpExchange):
    request_qp = {k: v for k, v in exchange.request.query_params.items()}
    http_url = exchange.request.http_url
    if request_qp:
        http_url = http_url + "?" + dict_formatter(request_qp.items(), "{k}={v}", "&")

    request_headers = dict_formatter(
        exchange.request.headers.items(), "{k}: {v}", splitter="\n"
    )

    formatted_request_body = highlight_format_json(
        exchange.request.request_body, formatter=NullFormatter()
    )

    return f"""
**{exchange.request.http_method} {http_url}**
```
{request_headers}
```
```
{formatted_request_body or " "}
```    
    """


def markdown_response(exchange: HttpExchange):
    elapsed_time = elapsed_time_formatter(exchange.response.elapsed_time)
    if exchange.response.is_mocked:
        elapsed_time = "Mocked Response"

    response_headers = dict_formatter(
        exchange.response.headers.items(), "{k}: {v}", splitter="\n"
    )

    formatted_response_body = highlight_format_json(
        exchange.response.response_body, formatter=NullFormatter()
    )
    return f"""
**HTTP {exchange.response.http_status_code} ({elapsed_time})**
```
{response_headers}
```
```json
{formatted_response_body or " "}
```
    """
