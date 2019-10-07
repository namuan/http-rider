import attr
from pygments.lexers.python import Python3Lexer
from typing import List

from ..core.core_settings import app_settings
from ..exporters import *
from ..model.app_data import ApiCall


def to_python_requests(api_call, last_exchange):
    func_name = get_function_name(api_call)
    method = last_exchange.request.http_method
    url = last_exchange.request.http_url
    has_qp = True if last_exchange.request.query_params else False
    query_params = dict_formatter(
        last_exchange.request.query_params.items(),
        "\"{k}\": \"{v}\""
    )
    has_headers = True if last_exchange.request.headers else False
    headers = dict_formatter(
        last_exchange.request.headers.items(),
        "\"{k}\": \"{v}\"",
        splitter=",\n"
    )
    has_json_body = True if last_exchange.request.request_body else False

    json_body = "data=\"{}\"".format(
        encode_json_string(last_exchange.request.request_body) if has_json_body else "")

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
    py_func = f"""
def {func_name}():
    try:
        response = requests.{method.lower()}(
                url="{url}",
                {params_code if has_qp else ""}
                {headers_code if has_headers else ""}
                {json_body if has_json_body else ""}
        )
        print(f'Response HTTP Status Code: {{response.status_code}}')
        print(f'Response HTTP Response Body: {{response.content}}')
    except requests.exceptions.RequestException as e:
        print(f'HTTP Request failed {{e}}')
    """
    return py_func


@attr.s
class PythonRequestsExporter:
    name: str = "Python (Requests)"
    output_ext: str = "py"

    def export_data(self, api_calls: List[ApiCall]):
        file_header = """
# Install the Python Requests library

import requests
import json
import random
import string
import uuid

        """
        output = [
            self.__export_api_call(api_call)
            for api_call in api_calls
        ]
        return highlight(file_header, Python3Lexer(), HtmlFormatter()) + "<br/>".join(output)

    def __export_api_call(self, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        doc = f"""# {api_call.title}
# 
{to_python_requests(api_call, last_exchange)}
"""
        return highlight(doc, Python3Lexer(), HtmlFormatter())


exporter = PythonRequestsExporter()
