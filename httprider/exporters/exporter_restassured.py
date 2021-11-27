import attr
from pygments.lexers.jvm import JavaLexer
from typing import List

from httprider.core.core_settings import app_settings
from httprider.exporters.common import *
from httprider.model.app_data import (
    ApiCall,
    HttpExchange,
    ApiTestCase,
    AssertionDataSource,
)
from httprider.codegen.schema_to_java_generator import to_java_function_name


def gen_given(api_call: ApiCall, last_exchange: HttpExchange):
    statements = ["\tgiven()."]
    statements.append(
        dict_formatter(
            last_exchange.request.headers.items(),
            '                header("{k}", "{v}").',
            splitter="\n",
        )
    )

    if last_exchange.request.request_body:
        encoded_json_string = encode_json_string(last_exchange.request.request_body)
        statements.append(f'                body("{encoded_json_string}").')

    if len(statements) == 0:
        return ""

    return "\n".join(statements)


def gen_when(api_call: ApiCall, last_exchange: HttpExchange):
    statements = [
        "\twhen().",
        f'                request("{last_exchange.request.http_method}", "{last_exchange.request.http_url}")',
    ]
    return "\n".join(statements)


def gen_then(
    api_call: ApiCall, last_exchange: HttpExchange, api_test_case: ApiTestCase
):
    statements = ["\tthen()."]
    for a in api_test_case.assertions:
        if a.data_from == AssertionDataSource.RESPONSE_CODE.value:
            statements.append(f"                statusCode({converter(a)})")

        if a.data_from == AssertionDataSource.RESPONSE_HEADER.value:
            statements.append(
                f'                header("{a.selector}", "{converter(a)}")'
            )

        if a.data_from == AssertionDataSource.RESPONSE_BODY.value:
            statements.append(f'                body("{a.selector}", "{converter(a)}")')

    if len(statements) == 1:
        return ""

    return "\n".join(statements)


def converter(assertion):
    return (
        "exist"
        if assertion.expected_value == "Not Null"
        else f"{assertion.expected_value}"
    )


def gen_function(api_call, last_exchange, api_test_case):
    return f"""
    void {to_java_function_name(api_call.title)}() {{
{gen_given(api_call, last_exchange)}
{gen_when(api_call, last_exchange)}                
{gen_then(api_call, last_exchange, api_test_case)};
    }}
    """


@attr.s
class RestAssuredExporter:
    name: str = "Rest Assured"
    output_ext: str = "java"

    def export_data(self, api_calls: List[ApiCall]):
        test_file_header = """
/*
    Maven Dependencies
     
    <dependency>
        <groupId>io.rest-assured</groupId>
        <artifactId>rest-assured</artifactId>
        <version>3.0.0</version>
        <scope>test</scope>
    </dependency>

    Hamcrest Matchers
    
    <dependency>
        <groupId>org.hamcrest</groupId>
        <artifactId>hamcrest-all</artifactId>
        <version>1.3</version>
    </dependency>

    JSON Schema Validation
    
    <dependency>
        <groupId>io.rest-assured</groupId>
        <artifactId>json-schema-validator</artifactId>
        <version>4.0.0</version>
    </dependency>

*/

import io.restassured.RestAssured.*;
import io.restassured.matcher.RestAssuredMatchers.*;
import org.hamcrest.Matchers.*;

class AirHttpTests {   
        """
        test_file_footer = """
}        
        """
        output = [self.__export_api_call(api_call) for api_call in api_calls]
        return (
            highlight(test_file_header, JavaLexer(), HtmlFormatter())
            + "<br/>"
            + "<br/>".join(output)
            + "<br/>"
            + highlight(test_file_footer, JavaLexer(), HtmlFormatter())
        )

    def __export_api_call(self, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        api_test_case = app_settings.app_data_cache.get_api_test_case(api_call.id)
        doc = gen_function(api_call, last_exchange, api_test_case)
        return highlight(doc, JavaLexer(), HtmlFormatter())


exporter = RestAssuredExporter()
