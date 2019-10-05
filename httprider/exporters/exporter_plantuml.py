import attr
from pygments.lexers.jvm import JavaLexer
from typing import List

from ..core import schema_from_json
from ..core.core_settings import app_settings
from ..exporters import *
from ..model.app_data import ApiCall

regex = r'.*\[([\S\s]*)->([\S\s][^]]*)\](.*)$'


def get_actors_from_title(api_title):
    matched_tokens = re.search(regex, api_title)
    if matched_tokens:
        return matched_tokens.groups()
    return None, None, None


def gen_function(api_call, last_exchange, api_test_case, project_info):
    source, target, title = get_actors_from_title(api_call.title)
    api_uri = last_exchange.request.http_url
    if not source:
        return ""
    headers = dict_formatter(
        dict_items=last_exchange.request.headers.items(),
        form="{k}<font color=\"red\">*</font> //<string>//",
        splitter="\n"
    )
    query_params = dict_formatter(
        dict_items=last_exchange.request.query_params.items(),
        form="{k}<font color=\"red\">*</font> //<string>//",
        splitter="\n"
    )
    formatted_request_body = format_json(last_exchange.request.request_body)
    statements = [
        f"\"{source.strip()}\"->\"{target.strip()}\": **{last_exchange.request.http_method}** \"{api_uri}\"",
        f"rnote right {source.strip()}",
        f"{api_call.title}",
        f"",
        f"**Headers**",
        f"{headers}",
        f"**Query Params**",
        f"{query_params}",
        f"**Payload**",
        f"{formatted_request_body}",
        f"end note",
    ]

    return "\n".join(statements)


@attr.s
class PlantUmlExporter:
    name: str = "PlantUML Sequence Diagrams"
    output_ext: str = "puml"

    def export_data(self, api_calls: List[ApiCall]):
        test_file_header = """
To generate a sequence diagram, make sure that API Title is using the following syntax

[ ActorA -> ActorB ] Get product details

The above will generate the following syntax

@startuml
ActorA -> ActorB: Get product details
@enduml
            
"""
        sorted_apis_by_sequence = sorted(api_calls, key=lambda a: a.sequence_number or 0)

        output = [
            self.__export_api_call(api_call)
            for api_call in sorted_apis_by_sequence
        ]

        combined_output = "\n".join(output)

        if not combined_output.strip():
            return highlight(test_file_header, JavaLexer(), HtmlFormatter())

        complete_text = "@startuml\n" + combined_output + "\n@enduml"
        return highlight(complete_text, JavaLexer(), HtmlFormatter())

    def __export_api_call(self, api_call):
        project_info = app_settings.app_data_reader.get_or_create_project_info()
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        api_test_case = app_settings.app_data_cache.get_api_test_case(api_call.id)
        doc = gen_function(api_call, last_exchange, api_test_case, project_info)
        return doc


exporter = PlantUmlExporter()
