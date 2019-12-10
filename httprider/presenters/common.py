from pygments.formatters.other import NullFormatter

from httprider.core import elapsed_time_formatter
from httprider.exporters.common import dict_formatter, highlight_format_json
from httprider.model.app_data import HttpExchange


def markdown_request(exchange: HttpExchange):
    http_url = exchange.request.full_encoded_url

    request_headers = dict_formatter(
        exchange.request.headers.items(), "{k}: {v}", splitter="\n"
    )

    formatted_request_body = highlight_format_json(
        exchange.request.request_body, formatter=NullFormatter()
    )

    return f"""
**{exchange.request.http_method} {http_url}**
```sh
{request_headers}
```
```json
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
```sh
{response_headers}
```
```json
{formatted_response_body or " "}
```
    """


def md_request_response_generator(exchange: HttpExchange, include_sep=True):
    request_rendered = markdown_request(exchange)
    response_rendered = markdown_response(exchange)

    content = f"""### Request
{request_rendered}
### Response
{response_rendered}
{"=======================================================================================" if include_sep else ""}    
    """
    return content
