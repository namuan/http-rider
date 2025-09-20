import attr
from pygments.lexers.testing import GherkinLexer

from httprider.core import evaluate_nested_functions
from httprider.core.constants import AssertionMatchers
from httprider.core.core_settings import app_settings
from httprider.exporters.common import *
from httprider.model.app_data import (
    ApiCall,
    ApiTestCase,
    AssertionDataSource,
    HttpExchange,
    ProjectInfo,
)


def gen_tags(tags: list):
    return " ".join([f"@{t}" for t in tags])


def convert_internal_variable(str_with_variable):
    return internal_var_selector.sub(r"`\1`", str_with_variable, count=0) if str_with_variable else ""


def gen_given(api_call: ApiCall, last_exchange: HttpExchange):
    first_statement = True
    statements = []
    test_tags = gen_tags(api_call.tags)
    if test_tags:
        statements.append(f"{test_tags}")

    statements.append(f"Scenario: {api_call.title}")
    for hk, hv in api_call.enabled_headers().items():
        converted_hv = evaluate_nested_functions(convert_internal_variable(hv))
        if first_statement:
            statements.append(f"    Given I set {hk} header to {converted_hv}")
            first_statement = False
        else:
            statements.append(f"    And I set {hk} header to {converted_hv}")

    request_body = api_call.request_body_without_comments()
    if request_body:
        converted_request_body = evaluate_nested_functions(convert_internal_variable(request_body))
        if first_statement:
            statements.append(f"    Given I set body to {converted_request_body}")
            first_statement = False
        else:
            statements.append(f"    And I set body to {converted_request_body}")

    if not statements:
        return ""

    return "\n".join(statements)


def apickli_http_method(http_method: str):
    table = {"post": f"{http_method} to", "options": f"request {http_method} for"}
    return table.get(http_method.lower(), http_method)


def gen_when(project_info: ProjectInfo, api_call: ApiCall, last_exchange: HttpExchange):
    http_relative_uri = extract_uri(last_exchange.request.http_url, project_info.servers)
    method_conversion = apickli_http_method(last_exchange.request.http_method)
    statements = [f"    When I {method_conversion} {http_relative_uri}"]
    return "\n".join(statements)


def gen_then(api_call: ApiCall, last_exchange: HttpExchange, api_test_case: ApiTestCase):
    statements = [f"    Then response code should be {last_exchange.response.http_status_code}"]

    for a in api_test_case.assertions:
        if a.data_from == AssertionDataSource.RESPONSE_HEADER.value:
            statements.append(f"    And response header {a.selector} {converter(a)}")

        if a.data_from == AssertionDataSource.RESPONSE_BODY.value:
            statements.append(f"    And response body path {a.selector} {converter_path_statement(a)}")

    for a in api_test_case.variables():
        if a.data_from == AssertionDataSource.RESPONSE_HEADER.value:
            statements.append(f"    And I store the value of response header {a.selector} as {a.var_name}")

        if a.data_from == AssertionDataSource.RESPONSE_BODY.value:
            statements.append(f"    And I store the value of body path {a.selector} as {a.var_name} in global scope")

    return "\n".join(statements)


def converter(assertion):
    return (
        "should exist"
        if assertion.matcher in [AssertionMatchers.NOT_NULL.value, AssertionMatchers.NOT_EMPTY.value]
        else f"should be {assertion.expected_value}"
    )


def converter_path_statement(assertion):
    return (
        "should not be empty"
        if assertion.matcher in [AssertionMatchers.NOT_NULL.value, AssertionMatchers.NOT_EMPTY.value]
        else f"should be {assertion.expected_value}"
    )


@attr.s
class ApickliExporter:
    name: str = "Apickli Tests"
    output_ext: str = "text"

    def export_data(self, api_calls: list[ApiCall]):
        test_file_header = """
## See https://github.com/namuan/apickli_functional_tests for starting up a new project.

## The following feature definitions should go in tests/Functional.feature file.

Feature: Validating API requests
    As a user, I want to validate that all the user scenarios are correct
"""
        project_info = app_settings.app_data_reader.get_or_create_project_info()

        output = [self.__export_api_call(project_info, api_call) for api_call in api_calls]

        return highlight(test_file_header, GherkinLexer(), HtmlFormatter()) + "<br/>".join(output)

    def __export_api_call(self, project_info, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        api_test_case = app_settings.app_data_cache.get_api_test_case(api_call.id)
        doc = f"""# {api_call.title}
#
{gen_given(api_call, last_exchange)}
{gen_when(project_info, api_call, last_exchange)}
{gen_then(api_call, last_exchange, api_test_case)}
"""
        return highlight(doc, GherkinLexer(), HtmlFormatter())


exporter = ApickliExporter()
