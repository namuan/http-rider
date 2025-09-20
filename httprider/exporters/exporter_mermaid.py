import re

import attr
from pygments.lexers.jvm import JavaLexer

from httprider.core.core_settings import app_settings
from httprider.exporters.common import *
from httprider.model.app_data import ApiCall

regex = r".*\[([\S\s]*)->([\S\s][^]]*)\](.*)$"


def get_actors_from_title(api_title):
    matched_tokens = re.search(regex, api_title)
    if matched_tokens:
        return matched_tokens.groups()
    return None, None, None


def gen_function(api_call, last_exchange, api_test_case):
    source, target, _title = get_actors_from_title(api_call.title)
    if not source:
        return ""

    statements = [
        f"    {source.strip()}->>{target.strip()}: {last_exchange.request.http_method} {last_exchange.request.http_url}",
    ]

    return "\n".join(statements)


@attr.s
class MermaidExporter:
    name: str = "Mermaid Sequence Diagrams"
    output_ext: str = "mm"

    def export_data(self, api_calls: list[ApiCall]):
        test_file_header = """
To generate a sequence diagram, make sure that API Title is using the following syntax

[ ActorA -> ActorB ] Get product details

The above will generate the following syntax

sequenceDiagram
    ActorA ->> ActorB: Get product details
"""
        sorted_apis_by_sequence = sorted(api_calls, key=lambda a: a.sequence_number or 0)

        output = [self.__export_api_call(api_call) for api_call in sorted_apis_by_sequence]

        combined_output = "\n".join(output)

        if not combined_output.strip():
            return highlight(test_file_header, JavaLexer(), HtmlFormatter())

        complete_text = "sequenceDiagram\n" + combined_output
        return highlight(complete_text, JavaLexer(), HtmlFormatter())

    def __export_api_call(self, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        api_test_case = app_settings.app_data_cache.get_api_test_case(api_call.id)
        return gen_function(api_call, last_exchange, api_test_case)


exporter = MermaidExporter()
