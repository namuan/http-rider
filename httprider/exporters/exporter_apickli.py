import attr
from pygments.lexers.testing import GherkinLexer
from typing import List

from ..core.core_settings import app_settings
from ..exporters import *
from ..model.app_data import ApiCall, HttpExchange, ApiTestCase, AssertionDataSource


def gen_given(api_call: ApiCall, last_exchange: HttpExchange):
    first_statement = True
    statements = []
    for hk, hv in last_exchange.request.headers.items():
        if first_statement:
            statements.append(f"    Given I set {hk} header to {hv}")
            first_statement = False
        else:
            statements.append(f"    And I set {hk} header to {hv}")

    if not statements:
        return ""

    return "\n".join(statements)


def gen_when(api_call: ApiCall, last_exchange: HttpExchange):
    statements = [
        f"    When I request {last_exchange.request.http_method} for {last_exchange.request.http_url}"
    ]
    return "\n".join(statements)


def gen_then(api_call: ApiCall, last_exchange: HttpExchange, api_test_case: ApiTestCase):
    statements = [
        f"    Then response code should be {last_exchange.response.http_status_code}"
    ]

    for a in api_test_case.assertions:
        if a.data_from == AssertionDataSource.RESPONSE_HEADER.value:
            statements.append(f"    And response header {a.selector} should {converter(a)}")

        if a.data_from == AssertionDataSource.RESPONSE_BODY.value:
            statements.append(f"    And response path {a.selector} should {converter(a)}")

    for a in api_test_case.assertions:
        if a.data_from == AssertionDataSource.RESPONSE_HEADER.value:
            statements.append(f"    And I store the value of response header {a.selector} as {a.var_name}")

        if a.data_from == AssertionDataSource.RESPONSE_BODY.value:
            statements.append(f"    And I store the value of body path {a.selector} as {a.var_name}")

    return "\n".join(statements)


def converter(assertion):
    return "exist" if assertion.expected_value == "Not Null" else f"be {assertion.expected_value}"


@attr.s
class ApickliExporter:
    name: str = "Apickli Tests"
    output_ext: str = "text"

    def export_data(self, api_calls: List[ApiCall]):
        test_file_header = """
## See https://github.com/namuan/apickli_functional_tests for starting up a new project. 

## The following feature definitions should go in tests/Functional.feature file.           

Feature Validating API requests
    As a user, I want to validate that all the user scenarios are correct
"""
        output = [
            self.__export_api_call(api_call)
            for api_call in api_calls
        ]

        return highlight(test_file_header, GherkinLexer(), HtmlFormatter()) + "<br/>".join(output)

    def __export_api_call(self, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        api_test_case = app_settings.app_data_cache.get_api_test_case(api_call.id)
        doc = f"""# {api_call.title}
# 
{gen_given(api_call, last_exchange)}
{gen_when(api_call, last_exchange)}
{gen_then(api_call, last_exchange, api_test_case)}
"""
        return highlight(doc, GherkinLexer(), HtmlFormatter())


exporter = ApickliExporter()
