import attr
from pygments.lexers.python import Python3Lexer

from httprider.core import ContentType
from httprider.core.core_settings import CoreSettings, app_settings
from httprider.exporters.common import *
from httprider.model.app_data import ApiCall


def to_python_requests(idx, api_call: ApiCall, last_exchange: HttpExchange):
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

    py_func = f"""
    @task
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
        print_details("{func_name}", response)
    """
    return py_func


@attr.s(auto_attribs=True)
class LocustTestsExporter:
    app_config: CoreSettings
    name: str = "Locust (Performance Tests)"
    output_ext: str = "py"

    def export_data(self, api_calls: list[ApiCall], return_raw=False):
        file_header = """
# python3 -m pip install locust - See https://docs.locust.io/en/stable/installation.html
# python3 -m pip install Faker - See https://faker.readthedocs.io/en/master/
# Running the tests with web ui
# locust -f this_file.py
# Or to run it without web ui for 20(secs) with 10 users and 2 users to spawn every second
# locust -f locust_test.py --headless --users 10 --hatch-rate 2 --run-time 20s

from locust import HttpUser, SequentialTaskSet, constant, constant_pacing, between, task
import json
import random
import string
import uuid
from faker import Faker
from datetime import datetime

fake = Faker()

def fake_person():
    return fake.name()

def random_uuid():
    return str(uuid.uuid4())

def random_str(length=10, with_punctuation=False):
    selection = string.ascii_letters + string.digits
    selection = selection + string.punctuation if with_punctuation else selection
    return ''.join(random.choice(selection) for i in range(length))

def random_int(min=0, max=100):
    return random.randint(min, max)

def bold(message):
    return f"\\033[1m{message}\\033[0m"

def print_details(tag, response):
    request_dt = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"{bold(tag)} request date time:{request_dt}")
    print(
        f" {bold('Status Code:')} {response.status_code}  {bold('Response:')} {response.json()}"
    )

class ApiTestSteps(SequentialTaskSet):
        """

        file_footer = """
class ApiUser(HttpUser):
    tasks = [ApiTestSteps]
    host = "localhost"

    # See https://docs.locust.io/en/stable/api.html#locust.wait_time
    wait_time = constant(1) # wait between requests. Other options between(5, 15) or constant_pacing(1)

        """
        output = [self.__export_api_call(idx, api_call) for idx, api_call in enumerate(api_calls)]
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
