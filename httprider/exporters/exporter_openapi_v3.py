import logging
import operator
from itertools import groupby
from typing import List

import attr
from apispec import APISpec

from ..core import schema_from_json
from ..core.core_settings import app_settings
from ..exporters import highlight, data, HtmlFormatter
from ..model.app_data import ApiCall, ProjectInfo, HttpExchange, ExchangeRequest, ExchangeResponse


@attr.s
class OpenApiv3Exporter:
    name: str = "OpenAPI(v3)"
    output_ext: str = "yml"

    def export_data(self, api_calls: List[ApiCall]):
        project_info = app_settings.app_data_reader.get_or_create_project_info()
        spec = self.init_spec(project_info)

        # Combine API calls with same url
        sorted_api_calls = sorted(api_calls, key=operator.attrgetter('http_url'))
        grouped_data = groupby(sorted_api_calls, key=operator.attrgetter('http_url'))

        api_call_tags = []

        for api_path, apis in grouped_data:
            grouped_apis = list(apis)
            self.export_api_calls(spec, api_path, grouped_apis, project_info.servers)
            for api in grouped_apis:
                if api.tags:
                    api_call_tags.append(*api.tags)

        for tag in project_info.tags:
            if tag.name in api_call_tags:
                spec.tag(dict(
                    name=tag.name,
                    description=tag.description
                ))

        return highlight(spec.to_yaml(), data.YamlLexer(), HtmlFormatter())

    def init_spec(self, project_info: ProjectInfo):
        return APISpec(
            title=project_info.title,
            version=project_info.version,
            openapi_version="3.0.2",
            info=dict(
                description=project_info.info
            ),
            servers=[{'url': s} for s in project_info.servers]
        )

    def extract_uri(self, url, servers):
        matched_server = next((server for server in servers if url.startswith(server)), None)
        if matched_server:
            return url.replace(matched_server, "")

        return url

    def export_api_calls(self, api_spec, api_path, api_calls, servers):
        # api_call = api_calls[0]
        # last_exchange = app_settings.app_data_reader.get_last_exchange(api_call.id)
        # http_relative_uri = self.extract_uri(last_exchange.request.http_url, servers)
        http_relative_uri = self.extract_uri(api_path, servers)

        operations = {}

        for api in api_calls:
            http_method = api.http_method.lower()
            logging.debug(f"Exporting API Path: {http_method} {api_path}: API calls: {len(api_calls)}")

            operations[http_method] = operations.get(http_method) or {
                'summary': api.title,
                'tags': []
            }

            if api.tags:
                operations[http_method]['tags'].append(*api.tags)

            parameters = []
            self.add_params(parameters, api.http_headers, 'header')
            self.add_params(parameters, api.http_params, 'query')

            if parameters:
                operations[http_method]['parameters'] = parameters

            last_exchange = app_settings.app_data_cache.get_last_exchange(api.id)

            # Request object
            if last_exchange.request.request_body:
                operations[http_method]['requestBody'] = operations[http_method].get('requestBody', {})
                operations[http_method]['requestBody']['content'] = \
                    operations[http_method]['requestBody'].get('content', {})

                request_content_type = last_exchange.request.content_type()
                operations[http_method]['requestBody']['content'][request_content_type] \
                    = schema_from_json(last_exchange.request.request_body)

            # Response object
            response_code = last_exchange.response.http_status_code
            if response_code:
                operations[http_method]['responses'] = {
                    response_code: {
                        "description": "Map Status Code to Description Here"
                    }
                }

                if last_exchange.response.response_body:
                    generated_response_schema = schema_from_json(last_exchange.response.response_body)
                    response_content_type = last_exchange.response.content_type()

                    operations[http_method]['responses'][response_code]['content'] = {
                        response_content_type: generated_response_schema
                    }

        # Build spec
        api_spec.path(
            http_relative_uri,
            operations=operations
        )

    def add_params(self, parameters, source_params, params_type):
        for param, param_value in source_params.items():
            parameters.append({
                'name': param,
                'in': params_type,
                'schema': {
                    'type': 'string',
                    'example': param_value.display_text
                }
            })


exporter = OpenApiv3Exporter()

if __name__ == '__main__':
    try:
        spec = APISpec(
            title="A Super simple API",
            version="1.0.0",
            openapi_version="3.0.2"
        )
        api_call = ApiCall(
            id=2,
            description='Httpbin call to get request data - df92df60-c1b1-46fe-b83d-220e22ba152a',
            title='Get httpbin',
            http_url='${API_URL}/get',
            http_method='GET',
            http_headers={},
            http_params={},
            form_params={},
            http_request_body='',
            sequence_number=1000,
            type='api',
            tags=['Registration'],
            last_response_code=200,
            enabled=True
        )
        last_exchange = HttpExchange(
            api_call_id=2,
            id=5,
            request=ExchangeRequest(
                request_time='Thu Jun 20 09:04:55 2019',
                http_method='GET',
                http_url='http://127.0.0.1:8000/get',
                headers={},
                query_params={},
                form_params={},
                request_body=''
            ),
            type='http_exchange',
            response=ExchangeResponse(
                http_status_code=200,
                response_headers={'server': 'gunicorn/19.9.0', 'date': 'Thu, 20 Jun 2019 08:04:55 GMT',
                                  'connection': 'close', 'content-type': 'application/json', 'content-length': '273',
                                  'access-control-allow-origin': '*', 'access-control-allow-credentials': 'true'},
                response_body='{\n  "args": {}, \n  "headers": {\n    "Accept": "*/*", \n    "Accept-Encoding": "gzip, deflate", \n    "Connection": "keep-alive", \n    "Host": "127.0.0.1:8000", \n    "User-Agent": "python-requests/2.21.0"\n  }, \n  "origin": "127.0.0.1", \n  "url": "http://127.0.0.1:8000/get"\n}\n',
                response_time=236.53099999999998),
            assertions=[]
        )
    except SyntaxError as e:
        print("Gracefully handling syntax error")
