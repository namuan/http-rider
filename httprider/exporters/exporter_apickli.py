from typing import List

import attr
from pygments.lexers.testing import GherkinLexer

from ..core.core_settings import app_settings
from ..exporters import *
from ..model.app_data import ApiCall, HttpExchange, ApiTestCase, AssertionDataSource


def gen_given(api_call: ApiCall, last_exchange: HttpExchange):
    statements = ["GIVEN:"]
    for hk, hv in last_exchange.request.headers.items():
        statements.append(f"    I set {hk} header to {hv}")

    if len(statements) == 1:
        return ""

    return "\n".join(statements)


def gen_when(api_call: ApiCall, last_exchange: HttpExchange):
    statements = [
        "WHEN:",
        f"    I request {last_exchange.request.http_method} for {last_exchange.request.http_url}"
    ]
    return "\n".join(statements)


def gen_then(api_call: ApiCall, last_exchange: HttpExchange, api_test_case: ApiTestCase):
    statements = ["THEN:"]
    for a in api_test_case.assertions:
        if a.data_from == AssertionDataSource.RESPONSE_CODE.value:
            statements.append(f"    response code should {converter(a)}")

        if a.data_from == AssertionDataSource.RESPONSE_HEADER.value:
            statements.append(f"    response header {a.selector} should {converter(a)}")

        if a.data_from == AssertionDataSource.RESPONSE_BODY.value:
            statements.append(f"    response path {a.selector} should {converter(a)}")

    for a in api_test_case.assertions:
        if a.data_from == AssertionDataSource.RESPONSE_HEADER.value:
            statements.append(f"    I store the value of response header {a.selector} as {a.var_name}")

        if a.data_from == AssertionDataSource.RESPONSE_BODY.value:
            statements.append(f"    I store the value of body path {a.selector} as {a.var_name}")

    if len(statements) == 1:
        return ""

    return "\n".join(statements)


def converter(assertion):
    return "exist" if assertion.expected_value == "Not Null" else f"be {assertion.expected_value}"


@attr.s
class ApickliExporter:
    name: str = "Apickli Tests"
    output_ext: str = "text"

    def export_data(self, api_calls: List[ApiCall]):
        output = [
            self.__export_api_call(api_call)
            for api_call in api_calls
        ]
        return "<br/>".join(output)

    def __export_api_call(self, api_call):
        last_exchange = app_settings.app_data_reader.get_last_exchange(api_call.id)
        api_test_case = app_settings.app_data_reader.get_api_test_case(api_call.id)
        doc = f"""# {api_call.title}
# 
{gen_given(api_call, last_exchange)}
{gen_when(api_call, last_exchange)}
{gen_then(api_call, last_exchange, api_test_case)}
"""
        return highlight(doc, GherkinLexer(), HtmlFormatter())


exporter = ApickliExporter()
