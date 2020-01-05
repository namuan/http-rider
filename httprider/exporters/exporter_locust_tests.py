from typing import List

import attr
from pygments.lexers.python import Python3Lexer

from httprider.core import ContentType
from httprider.core.core_settings import app_settings, CoreSettings
from httprider.exporters.common import *
from httprider.model.app_data import ApiCall


def to_python_requests(idx, api_call: ApiCall, last_exchange: HttpExchange):
    func_name = get_function_name(api_call)
    method = last_exchange.request.http_method
    url = last_exchange.request.http_url
    has_qp = True if last_exchange.request.query_params else False
    query_params = dict_formatter(
        last_exchange.request.query_params.items(), '"{k}": "{v}"'
    )
    has_headers = True if last_exchange.request.headers else False
    headers = dict_formatter(
        last_exchange.request.headers.items(), '"{k}": "{v}"', splitter=",\n"
    )
    request_body_type = last_exchange.request.request_body_type
    request_body = None
    if request_body_type == ContentType.FORM:
        request_body = "data={}".format(last_exchange.request.form_params)
    elif request_body_type == ContentType.JSON:
        has_json_body = True if last_exchange.request.request_body else False
        request_body = "json={}".format(
            last_exchange.request.request_body if has_json_body else ""
        )

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
    @seq_task({idx + 1})
    # @task(10) # To run this test 10 times
    def {func_name}(self):
        # Group requests if it contains variable params
        # self.client.get("/api?id=%i" % i, name="/api?id=[id]")
        response = self.client.{method.lower()}(
                "{url}",
                {params_code if has_qp else ""}
                {headers_code if has_headers else ""}
                {request_body if request_body else ""}
        )
        print(f'Response HTTP Status Code: {{response.status_code}}')
    """
    return py_func


@attr.s(auto_attribs=True)
class LocustTestsExporter:
    app_config: CoreSettings
    name: str = "Locust (Performance Tests)"
    output_ext: str = "py"

    def export_data(self, api_calls: List[ApiCall], return_raw=False):
        file_header = """
# python3 -m pip install locustio - See https://docs.locust.io/en/stable/installation.html
# Running the tests with web ui
# locust -f this_file.py
# Or to run it without web ui for 20(secs) with 10 users and 2 users to spawn every second
# locust -f locust_test.py --no-web -c 10 -r 2 --run-time 20s

from locust import HttpLocust, TaskSet, TaskSequence, seq_task
import json
import random
import string
import uuid

def random_uuid():
    return str(uuid.uuid4())
    
def random_str(length=10, with_punctuation=False):
    selection = string.ascii_letters + string.digits
    selection = selection + string.punctuation if with_punctuation else selection
    return ''.join(random.choice(selection) for i in range(length))
    
def random_int(min=0, max=100):
    return random.randint(min, max)
    
class ApiTestSteps(TaskSequence):
        """
        file_footer = """
class ApiUser(HttpLocust):
    task_set = ApiTestSteps
    host = "localhost"
        
        """
        output = [
            self.__export_api_call(idx, api_call)
            for idx, api_call in enumerate(api_calls)
        ]
        unformatted_code = file_header + "\n".join(output) + file_footer
        formatted_code, _ = format_python_code(unformatted_code)

        return formatted_code if return_raw else highlight(formatted_code, Python3Lexer(), HtmlFormatter())

    def __export_api_call(self, idx, api_call):
        last_exchange = self.app_config.app_data_cache.get_last_exchange(api_call.id)
        doc = f"""
    # {api_call.title}
    {to_python_requests(idx, api_call, last_exchange)}
"""
        return doc


exporter = LocustTestsExporter(app_config=app_settings)
