from typing import List

import attr
from pygments.lexers.jvm import JavaLexer

from ..codegen.http_status_code_mapping import Languages, to_http_status
from ..codegen.schema_to_java_generator import (
    code_from_schema,
    to_java_class_name,
    to_java_function_name,
)
from ..core.core_settings import app_settings
from ..core.json_schema import schema_from_json
from ..exporters.common import *
from ..model.app_data import ApiCall, HttpExchange, ApiTestCase


def to_spring_http_method(http_method: str):
    if http_method.lower() not in ["options", "head"]:
        return f"@{to_java_class_name(http_method)}Mapping"
    else:
        return f"@GetMapping"


def to_spring_response_status(http_status_code):
    status, message = to_http_status(http_status_code, Languages.JAVA)
    return status, message, http_status_code


def gen_feign_client_request_class(
    api_call: ApiCall, last_exchange: HttpExchange, api_test_case: ApiTestCase
):
    if not last_exchange.request.request_body:
        return ""

    request_json_schema = schema_from_json(last_exchange.request.request_body)
    request_clazz_header = """
// Feign Client Request
    """
    clazz_definition = code_from_schema("ApiRequest", request_json_schema.get("schema"))
    return request_clazz_header + "\n" + clazz_definition


def gen_feign_client_response_class(
    api_call: ApiCall, last_exchange: HttpExchange, api_test_case: ApiTestCase
):
    if not last_exchange.response.response_body:
        return ""

    response_json_schema = schema_from_json(last_exchange.response.response_body)
    response_clazz_header = """
// Feign Client Response
    """
    clazz_definition = code_from_schema(
        "ApiResponse", response_json_schema.get("schema")
    )
    return response_clazz_header + "\n" + clazz_definition


def gen_feign_client_class(
    api_call: ApiCall, last_exchange: HttpExchange, api_test_case: ApiTestCase
):
    api_uri = ""
    has_request = ""  # true/false
    request_media_type = ""
    has_response = ""  # true/false
    response_media_type = ""
    mapping = to_spring_http_method(api_call.http_method)
    resp_status, resp_message, resp_code = to_spring_response_status(
        last_exchange.response.http_status_code
    )
    function_name = to_java_function_name(api_call.title)
    mapping_annotations = []
    mapping_annotations.append(f'value = "{api_uri}"')
    if has_request:
        mapping_annotations.append(f'consumes = "{request_media_type}"')
    if has_response:
        mapping_annotations.append(f'produces = "{response_media_type}"')

    feign_clazz = f"""
    {mapping}({",".join(mapping_annotations)})
    ApiResponse {function_name}(ApiRequest apiRequest);
    """

    return feign_clazz


@attr.s
class JavaFeignClientExporter:
    name: str = "Feign Client (Java)"
    output_ext: str = "java"

    def export_data(self, api_calls: List[ApiCall]):
        file_header = """
/*
    
    Java Feign Client
    Add following dependency If using with Spring
    implementation 'org.springframework.cloud:spring-cloud-starter-openfeign'
    
    Also remember to add the following annotation so that the client can be picked up by Spring
    @EnableFeignClients(clients = {HttpRiderFeignClient.class})
*/

package com.namuan.httprider;

import feign.RequestInterceptor;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.context.annotation.Bean;
import org.springframework.web.bind.annotation.*;

@FeignClient(name = "httpriderClient", url = "${target.url}", configuration = {HttpRiderClient.CustomConfig.class})
public interface HttpRiderFeignClient {{

    class CustomConfig {
        @Bean
        public RequestInterceptor headerInterceptor() {
            return template -> template.header("Food", "Bar");
        }
    }
"""
        file_footer = """

}}     
"""
        project_info = app_settings.app_data_reader.get_or_create_project_info()
        output = [
            self.__export_api_call(project_info, api_call) for api_call in api_calls
        ]

        return (
            highlight(file_header, JavaLexer(), HtmlFormatter())
            + "<br/>".join(output)
            + "<br/>"
            + highlight(file_footer, JavaLexer(), HtmlFormatter())
        )

    def __export_api_call(self, project_info, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        api_test_case = app_settings.app_data_cache.get_api_test_case(api_call.id)
        api_uri = last_exchange.request.http_url
        response_code = last_exchange.response.http_status_code
        formatted_request_body = format_json(last_exchange.request.request_body)
        formatted_response_body = format_json(last_exchange.response.response_body)
        doc = f"""    
{gen_feign_client_class(api_call, last_exchange, api_test_case)}
{gen_feign_client_request_class(api_call, last_exchange, api_test_case)}
{gen_feign_client_response_class(api_call, last_exchange, api_test_case)}

"""
        return highlight(doc, JavaLexer(), HtmlFormatter())


exporter = JavaFeignClientExporter()
