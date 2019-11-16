import attr
from pygments.lexers.jvm import JavaLexer
from typing import List

from ..codegen.http_status_code_mapping import Languages, to_http_status
from ..codegen.schema_to_java_generator import (
    code_from_schema,
    to_java_class_name,
    to_java_function_name,
)
from ..core import schema_from_json
from ..core.constants import AssertionMatchers
from ..core.core_settings import app_settings
from ..exporters import *
from ..model.app_data import ApiCall, HttpExchange, ApiTestCase, ProjectInfo, Assertion


def gen_tags(tags: List):
    return " ".join([f"@{t}" for t in tags])


def convert_internal_variable(str_with_variable):
    return (
        internal_var_selector.sub(r"`\1`", str_with_variable, count=0)
        if str_with_variable
        else ""
    )


def to_spring_http_method(http_method: str):
    if http_method.lower() not in ["options", "head"]:
        return f"@{to_java_class_name(http_method)}Mapping"
    else:
        return f"@GetMapping"


def to_mock_mvc_http_method(http_method: str):
    return http_method.lower()


def to_spring_response_status(http_status_code):
    status, message = to_http_status(http_status_code, Languages.JAVA)
    return status, message, http_status_code


def gen_api_request_class(
    api_call: ApiCall, last_exchange: HttpExchange, api_test_case: ApiTestCase
):
    if not last_exchange.request.request_body:
        return ""

    request_json_schema = schema_from_json(last_exchange.request.request_body)
    request_clazz_header = """
// 2. API Request definition
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
    """
    clazz_definition = code_from_schema("ApiRequest", request_json_schema.get("schema"))
    return request_clazz_header + "\n" + clazz_definition


def gen_api_response_class(
    api_call: ApiCall, last_exchange: HttpExchange, api_test_case: ApiTestCase
):
    if not last_exchange.response.response_body:
        return ""

    response_json_schema = schema_from_json(last_exchange.response.response_body)
    response_clazz_header = """
// 3. API Response definition
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
    """
    clazz_definition = code_from_schema(
        "ApiResponse", response_json_schema.get("schema")
    )
    return response_clazz_header + "\n" + clazz_definition


def gen_controller(
    api_call: ApiCall, last_exchange: HttpExchange, api_test_case: ApiTestCase
):
    mapping = to_spring_http_method(api_call.http_method)
    resp_status, resp_message, resp_code = to_spring_response_status(
        last_exchange.response.http_status_code
    )
    function_name = to_java_function_name(api_call.title)
    controller = f"""
// 4. Controller method
{mapping}(produces = MediaType.APPLICATION_JSON_VALUE)
@ResponseStatus({resp_status})
@ApiResponses({{
        @ApiResponse(code = {resp_code}, message = "{resp_message}")
}})
public ApiResponse {function_name}() {{    
    ApiResponse response = new ApiResponse();
    return response;    
}}
    """

    return controller


def to_json_result_matcher(a: Assertion):
    mapper = {
        AssertionMatchers.EQ.value: 'jsonPath("{}").value({})'.format(
            a.selector, a.expected_value
        )
        if a.var_type == "int"
        else 'jsonPath("{}").value("{}")'.format(a.selector, a.expected_value),
        AssertionMatchers.NOT_EQ.value: '!jsonPath("{}").value({})'.format(
            a.selector, a.expected_value
        )
        if a.var_type == "int"
        else 'jsonPath("{}").value("{}")'.format(a.selector, a.expected_value),
        AssertionMatchers.NOT_NULL.value: 'jsonPath("{}").exists()'.format(a.selector),
        AssertionMatchers.EMPTY.value: 'jsonPath("{}").isEmpty()'.format(a.selector),
        AssertionMatchers.NOT_EMPTY.value: 'jsonPath("{}").isNotEmpty()'.format(
            a.selector
        ),
        AssertionMatchers.CONTAINS.value: 'jsonPath("{}").value("//Hamcrest contains")'.format(
            a.selector
        ),
        AssertionMatchers.NOT_CONTAINS.value: '!jsonPath("{}").value("//Hamcrest contains")'.format(
            a.selector
        ),
        AssertionMatchers.LT.value: 'jsonPath("{}").value("//Hamcrest less than")'.format(
            a.selector
        ),
        AssertionMatchers.GT.value: 'jsonPath("{}").value("//Hamcrest greater than")'.format(
            a.selector
        ),
    }
    return mapper.get(a.matcher, None)


def gen_test_assertions(api_test_case: ApiTestCase):
    for assertion in api_test_case.comparable_assertions():
        yield ".andExpect({})".format(to_json_result_matcher(assertion))


def gen_test(
    api_call: ApiCall, last_exchange: HttpExchange, api_test_case: ApiTestCase
):
    mapping = to_mock_mvc_http_method(api_call.http_method)
    url = api_call.http_url
    resp_status, resp_code, resp_message = to_spring_response_status(
        last_exchange.response.http_status_code
    )
    function_name = to_java_function_name(api_call.title)
    encoded_json_string = encode_json_string(last_exchange.request.request_body)

    json_path_assertions = "\n".join(
        [statement for statement in gen_test_assertions(api_test_case)]
    )

    test_code = f"""
// 5. MockMvc test generator
// Add related imports here
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.*
// Add note on sample project

@Test
public void test{function_name}() throws Exception {{
    mockMvc.perform(
        {mapping}("{url}")
            .contentType(APPLICATION_JSON)
            .content("{encoded_json_string}"))
        .andExpect(status().is({resp_code}))
        {json_path_assertions}
        .andReturn();
}}
    """

    return test_code


def converter(assertion):
    return (
        "should exist"
        if assertion.matcher
        in [AssertionMatchers.NOT_NULL.value, AssertionMatchers.NOT_EMPTY.value]
        else f"should be {assertion.expected_value}"
    )


def converter_path_statement(assertion):
    return (
        "should not be empty"
        if assertion.matcher
        in [AssertionMatchers.NOT_NULL.value, AssertionMatchers.NOT_EMPTY.value]
        else f"should be {assertion.expected_value}"
    )


def gen_fox_config(project_info: ProjectInfo):
    output = f"""
// 1. SpringFox configuration
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.service.Contact;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger.web.*;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

import java.util.Collections;

@Configuration
@EnableSwagger2
public class SpringFoxConfiguration {{
    private ApiInfo apiInfo() {{
        return new ApiInfo(
                "{project_info.title}",
                "{project_info.info}",
                "{project_info.tos_url}",
                "Terms of service",
                new Contact("{project_info.contact_name}", "www.example.com", "{project_info.contact_email}"),
                "{project_info.license_name}",
                "{project_info.license_url}",
                Collections.emptyList());
    }}

    @Bean
    public Docket api() {{
        return new Docket(DocumentationType.SWAGGER_2)
                .apiInfo(apiInfo())
                .select()
                    .apis(RequestHandlerSelectors.any())
                    .paths(PathSelectors.any())
                .build();
    }}

    /**
     * SwaggerUI information
     */

    @Bean
    UiConfiguration uiConfig() {{
        return UiConfigurationBuilder.builder()
                .deepLinking(true)
                .displayOperationId(false)
                .defaultModelsExpandDepth(1)
                .defaultModelExpandDepth(1)
                .defaultModelRendering(ModelRendering.EXAMPLE)
                .displayRequestDuration(false)
                .docExpansion(DocExpansion.NONE)
                .filter(false)
                .maxDisplayedTags(null)
                .operationsSorter(OperationsSorter.ALPHA)
                .showExtensions(false)
                .tagsSorter(TagsSorter.ALPHA)
                .supportedSubmitMethods(UiConfiguration.Constants.DEFAULT_SUBMIT_METHODS)
                .validatorUrl(null)
                .build();
    }}
}}
    """
    return output


@attr.s
class SpringBootApiJavaExporter:
    name: str = "Spring Boot API (Java)"
    output_ext: str = "java"

    def export_data(self, api_calls: List[ApiCall]):
        test_file_header = """
/**
The generated code is divided into different sections
1. SpringFox configuration
2. Spring API request class
3. Spring API response class
4. Spring API controller definition
5. Unit testing with MockMvc
**/

"""
        project_info = app_settings.app_data_reader.get_or_create_project_info()
        fox_config = gen_fox_config(project_info)
        output = [
            self.__export_api_call(project_info, api_call) for api_call in api_calls
        ]

        return highlight(
            test_file_header + fox_config, JavaLexer(), HtmlFormatter()
        ) + "<br/>".join(output)

    def __export_api_call(self, project_info, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        api_test_case = app_settings.app_data_cache.get_api_test_case(api_call.id)
        doc = f"""
// {api_call.title}
{gen_api_request_class(api_call, last_exchange, api_test_case)}
{gen_api_response_class(api_call, last_exchange, api_test_case)}
{gen_controller(api_call, last_exchange, api_test_case)}
{gen_test(api_call, last_exchange, api_test_case)}
"""
        return highlight(doc, JavaLexer(), HtmlFormatter())


exporter = SpringBootApiJavaExporter()
