import logging
import operator
from itertools import groupby

import attr
from apispec import APISpec

from httprider.core.core_settings import CoreSettings, app_settings
from httprider.core.json_schema import schema_from_json
from httprider.exporters.common import *
from httprider.model.app_data import (
    ApiCall,
    ProjectInfo,
)


@attr.s(auto_attribs=True)
class OpenApiv3Exporter:
    app_config: CoreSettings
    name: str = "OpenAPI(v3)"
    output_ext: str = "yml"

    def export_data(self, api_calls: list[ApiCall], return_raw=False):
        project_info = self.app_config.app_data_reader.get_or_create_project_info()
        spec = self.init_spec(project_info)

        # Combine API calls with same url
        sorted_api_calls = sorted(api_calls, key=operator.attrgetter("http_url"))
        grouped_data = groupby(sorted_api_calls, key=operator.attrgetter("http_url"))

        api_call_tags = []

        for api_path, apis in grouped_data:
            grouped_apis = list(apis)
            self.export_api_calls(spec, api_path, grouped_apis, project_info.servers)
            for api in grouped_apis:
                if api.tags:
                    api_call_tags.extend(api.tags)

        for tag in project_info.tags:
            if tag.name in api_call_tags:
                spec.tag({"name": tag.name, "description": tag.description})

        return spec.to_yaml() if return_raw else highlight(spec.to_yaml(), data.YamlLexer(), HtmlFormatter())

    def init_spec(self, project_info: ProjectInfo):
        return APISpec(
            title=project_info.title,
            version=project_info.version,
            openapi_version="3.0.2",
            info={"description": project_info.info},
            servers=[{"url": s} for s in project_info.servers],
        )

    def export_api_calls(self, api_spec, api_path, api_calls, servers):
        http_relative_uri = self.url_from_last_exchange(api_calls, servers)
        # http_relative_uri = extract_uri(api_path, servers)

        operations = {}

        for api in api_calls:
            http_method = api.http_method.lower()
            logging.debug(f"Exporting API Path: {http_method} {api_path}: API calls: {len(api_calls)}")

            operations[http_method] = operations.get(http_method) or {
                "summary": api.title,
                "tags": [],
            }

            if api.tags:
                operations[http_method]["tags"].extend(api.tags)

            last_exchange = self.app_config.app_data_cache.get_last_exchange(api.id)

            parameters = []
            self.add_params(parameters, last_exchange.request.headers, "header")
            self.add_params(parameters, last_exchange.request.query_params, "query")

            if parameters:
                operations[http_method]["parameters"] = parameters

            # Request object
            if last_exchange.request.request_body:
                operations[http_method]["requestBody"] = operations[http_method].get("requestBody", {})
                operations[http_method]["requestBody"]["content"] = operations[http_method]["requestBody"].get(
                    "content", {}
                )

                request_content_type = last_exchange.request.content_type()
                operations[http_method]["requestBody"]["content"][request_content_type] = schema_from_json(
                    last_exchange.request.request_body
                )

            # Response object
            response_code = last_exchange.response.http_status_code
            if response_code:
                operations[http_method]["responses"] = {
                    response_code: {"description": "Map Status Code to Description Here"}
                }

                if last_exchange.response.response_body:
                    generated_response_schema = schema_from_json(
                        last_exchange.response.response_body, remove_required=True
                    )
                    response_content_type = last_exchange.response.content_type()

                    operations[http_method]["responses"][response_code]["content"] = {
                        response_content_type: generated_response_schema
                    }

        # Build spec
        api_spec.path(http_relative_uri, operations=operations)

    def url_from_last_exchange(self, api_calls, servers):
        api_call = api_calls[0]
        last_exchange = self.app_config.app_data_cache.get_last_exchange(api_call.id)
        http_relative_uri = extract_uri(last_exchange.request.http_url, servers)
        return http_relative_uri

    def add_params(self, parameters, source_params, params_type):
        for param, param_value in source_params.items():
            parameters.append({
                "name": param,
                "in": params_type,
                "schema": {"type": "string", "example": param_value},
            })


exporter = OpenApiv3Exporter(app_config=app_settings)
