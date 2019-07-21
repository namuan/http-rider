import json
import logging
from itertools import groupby
from operator import itemgetter

import attr
from apispec.core import VALID_METHODS_OPENAPI_V3
from prance import ResolvingParser

from httprider.core.app_state_interactor import AppStateInteractor
from ..core import DynamicStringData
from ..core.json_schema import json_from_schema
from ..model.app_data import ProjectInfo, TagInfo, ApiCall


@attr.s
class OpenApiV3Importer:
    name: str = "OpenApi(v3)"
    input_type: str = "file"
    app_state_interactor = AppStateInteractor()

    def import_data(self, file_path):
        openapi_spec: ResolvingParser = self.__load_swagger_spec(file_path)
        project_info = self.__extract_project_info(openapi_spec)
        base_path = project_info.servers[0] if project_info.servers else ""
        api_calls = self.__extract_api_calls(base_path, openapi_spec)
        return project_info, api_calls

    def __load_swagger_spec(self, file_path):
        return ResolvingParser(url=file_path)

    def __extract_project_info(self, openapi_spec):
        openapi_info = openapi_spec.specification["info"]
        openapi_tags = openapi_spec.specification["tags"]
        openapi_servers = openapi_spec.specification["servers"]
        info = ProjectInfo(
            info=openapi_info["description"].strip(),
            title=openapi_info["title"].strip(),
            version=openapi_info["version"].strip(),
            contact_email=openapi_info.get("contact", {}).get("email", "").strip(),
            contact_name=openapi_info.get("contact", {}).get("name", "").strip(),
            tags=[TagInfo(t["name"].strip(), t["description"].strip()) for t in openapi_tags],
            servers=[server.get("url", "") for server in openapi_servers]
        )
        return info

    def __extract_api_calls(self, base_path, openapi_spec):
        openapi_paths = openapi_spec.specification["paths"]
        return [
            self.__convert_to_api_call(base_path, path, path_spec, api_method, api_method_spec, content_type, schema)
            for path, path_spec in openapi_paths.items()
            for api_method, api_method_spec in path_spec.items()
            for content_type, schema in self.__request_content_types(api_method_spec).items()
            if api_method.strip().lower() in VALID_METHODS_OPENAPI_V3
        ]

    def __request_content_types(self, api_method_spec):
        has_request_body = type(api_method_spec) is dict \
                           and api_method_spec.get("requestBody", False) \
                           and api_method_spec.get("requestBody").get("content", False)

        if not has_request_body:
            return {None: None}
        else:
            return api_method_spec["requestBody"]["content"]

    def __process_parameters(self, path_spec, api_method_spec):
        path_params = path_spec.get("parameters", [])
        method_params = api_method_spec.get("parameters", [])
        all_params = path_params + method_params
        data = sorted(all_params, key=itemgetter("in"))
        grouped_data = groupby(data, key=itemgetter("in"))

        def params(pv):
            return {p["name"]: DynamicStringData(display_text="") for p in pv}

        gp = {k: params(data) for k, data in grouped_data}

        return gp.get("header", {}), gp.get("query", {}), gp.get("form", {})

    def __convert_to_api_call(self, base_path, path, path_spec, api_method, api_method_spec, content_type, schema):
        logging.info(f"Converting {api_method} - {content_type} - {path}")
        headers_params, query_params, form_params = self.__process_parameters(
            path_spec,
            api_method_spec
        )

        if content_type:
            headers_params["Content-Type"] = DynamicStringData(display_text=content_type)

        return ApiCall(
            tags=[t for t in api_method_spec.get("tags", [])],
            http_url=f"{base_path}{path}",
            http_method=api_method.upper(),
            title=api_method_spec.get("summary", ""),
            http_request_body=self.__extract_request_body(content_type, schema),
            description=api_method_spec.get("description", ""),
            http_headers=headers_params,
            http_params=query_params,
            form_params=form_params,
            sequence_number=self.app_state_interactor.update_sequence_number()
        )

    def __extract_request_body(self, content_type, schema):
        if schema:
            return json.dumps(json_from_schema(schema.get("schema")))

        return ""


importer = OpenApiV3Importer()
