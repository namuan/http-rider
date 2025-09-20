import attr
from pygments.lexers.python import Python3Lexer

from httprider.core import ContentType
from httprider.core.core_settings import app_settings
from httprider.exporters.common import *
from httprider.model.app_data import ApiCall


def to_python_requests(api_call, last_exchange):
    func_name = get_function_name(api_call)
    method = last_exchange.request.http_method
    url = last_exchange.request.http_url
    has_qp = bool(last_exchange.request.query_params)
    query_params = dict_formatter(last_exchange.request.query_params.items(), '"{k}": "{v}"')
    has_headers = bool(last_exchange.request.headers)
    headers = dict_formatter(last_exchange.request.headers.items(), '"{k}": "{v}"', splitter=",\n")
    request_body_type = last_exchange.request.request_body_type
    request_body = None
    if request_body_type == ContentType.FORM:
        request_body = f"data={last_exchange.request.form_params}"
    elif request_body_type == ContentType.JSON:
        has_json_body = bool(last_exchange.request.request_body)
        request_body = "json={}".format(last_exchange.request.request_body if has_json_body else "")

    params_code = f"""
    params={{
        {query_params if has_qp else ""}
    }},
    """

    headers_code = f"""
    headers={{
        {headers if has_headers else ""}
    }},
    """
    return f"""
def {func_name}():
    try:
        response = requests.{method.lower()}(
                url="{url}",
                {params_code if has_qp else ""}
                {headers_code if has_headers else ""}
                {request_body if request_body else ""}
        )
        print(f'Response HTTP Status Code: {{response.status_code}}')
        print(f'Response HTTP Response Body: {{response.content}}')
    except requests.exceptions.RequestException as e:
        print(f'HTTP Request failed {{e}}')
    """


@attr.s
class PythonRequestsExporter:
    name: str = "Python (Requests)"
    output_ext: str = "py"

    def export_data(self, api_calls: list[ApiCall]):
        file_header = """
# Install the Python Requests library

import requests
import json
import random
import string
import uuid

        """
        output = [self.__export_api_call(api_call) for api_call in api_calls]

        unformatted_code = file_header + "\n".join(output)
        formatted_code, _ = format_python_code(unformatted_code)
        return highlight(formatted_code, Python3Lexer(), HtmlFormatter())

    def __export_api_call(self, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        return f"""# {api_call.title}
{to_python_requests(api_call, last_exchange)}
"""


exporter = PythonRequestsExporter()
