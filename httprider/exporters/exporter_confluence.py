from typing import List

import attr
from pygments.lexers.markup import MarkdownLexer
from pygments.formatters.other import NullFormatter

from ..core.core_settings import app_settings
from ..exporters.common import *
from ..model.app_data import ApiCall


def gen_function(api_call, last_exchange, api_test_case):
    request_headers = dict_formatter(
        last_exchange.request.headers.items(), "{k}: {v}", splitter="\n"
    )
    response_headers = dict_formatter(
        last_exchange.response.headers.items(), "{k}: {v}", splitter="\n"
    )
    request_qp = {k: v for k, v in last_exchange.request.query_params.items()}
    http_url = last_exchange.request.http_url
    if request_qp:
        http_url = http_url + "?" + dict_formatter(request_qp.items(), "{k}={v}", "&")

    formatted_request_body = highlight_format_json(
        last_exchange.request.request_body, formatter=NullFormatter()
    )
    formatted_response_body = highlight_format_json(
        last_exchange.response.response_body, formatter=NullFormatter()
    )

    content = f"""
h3. {api_call.title}

{api_call.description}

h4. Request
{{code}}
{last_exchange.request.http_method} {http_url}
{{code}}
*Headers*
{{code}}
{request_headers}
{{code}}
*Body*
{{code}}
{formatted_request_body or " "}
{{code}}

h4. Response
{{code}}
HTTP {last_exchange.response.http_status_code}
{{code}}

*Headers*
{{code}}
{response_headers}
{{code}}

*Body*
{{code}}
{formatted_response_body or " "}
{{code}}
"""
    return content


@attr.s
class ConfluenceWikiExporter:
    name: str = "Confluence Wiki"
    output_ext: str = "txt"

    def export_data(self, api_calls: List[ApiCall]):
        output = [self.__export_api_call(api_call) for api_call in api_calls]

        combined_output = "\n".join(output)

        return highlight(combined_output, MarkdownLexer(), HtmlFormatter())

    def __export_api_call(self, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        api_test_case = app_settings.app_data_cache.get_api_test_case(api_call.id)
        return gen_function(api_call, last_exchange, api_test_case)


exporter = ConfluenceWikiExporter()
