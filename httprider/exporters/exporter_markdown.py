import attr
from pygments.formatters.other import NullFormatter
from pygments.lexers.markup import MarkdownLexer

from ..core.core_settings import app_settings
from ..exporters.common import *
from ..model.app_data import ApiCall


def gen_function(api_call, last_exchange, _api_test_case):
    request_headers = dict_formatter(last_exchange.request.headers.items(), "{k}: {v}", splitter="\n")
    response_headers = dict_formatter(last_exchange.response.headers.items(), "{k}: {v}", splitter="\n")
    request_qp = dict(last_exchange.request.query_params.items())
    http_url = last_exchange.request.http_url
    if request_qp:
        http_url = http_url + "?" + dict_formatter(request_qp.items(), "{k}={v}", "&")

    formatted_request_body = highlight_format_json(last_exchange.request.request_body, formatter=NullFormatter())
    formatted_response_body = highlight_format_json(last_exchange.response.response_body, formatter=NullFormatter())

    content = f"""
#### {api_call.title}

{api_call.description}

##### Request
```
{last_exchange.request.http_method} {http_url}
```
*Headers*
```
{request_headers}
```
*Body*
```
{formatted_request_body or " "}
```

##### Response
```
HTTP {last_exchange.response.http_status_code}
```

*Headers*
```
{response_headers}
```

*Body*
```
{formatted_response_body or " "}
```

*Sample Call*
```
{to_curl(api_call, last_exchange)}
```
"""
    return content


@attr.s
class MarkdownExporter:
    name: str = "Markdown Syntax"
    output_ext: str = "md"

    def export_data(self, api_calls: list[ApiCall]):
        output = [self.__export_api_call(api_call) for api_call in api_calls]

        combined_output = "\n".join(output)

        return highlight(combined_output, MarkdownLexer(), HtmlFormatter())

    def __export_api_call(self, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        api_test_case = app_settings.app_data_cache.get_api_test_case(api_call.id)
        return gen_function(api_call, last_exchange, api_test_case)


exporter = MarkdownExporter()
