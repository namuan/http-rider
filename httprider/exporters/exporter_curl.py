from typing import List

import attr
from pygments.lexers.shell import BashLexer

from ..core.core_settings import app_settings
from ..exporters import *
from ..model import to_curl
from ..model.app_data import ApiCall


@attr.s
class CurlExporter:
    name: str = "Curl"
    output_ext: str = "sh"

    def export_data(self, api_calls: List[ApiCall]):
        output = [
            self.__export_api_call(api_call)
            for api_call in api_calls
        ]
        return "<br/>".join(output)

    def __export_api_call(self, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        doc = f"""# {api_call.title}
# 
{to_curl(api_call, last_exchange)}
"""
        return highlight(doc, BashLexer(), HtmlFormatter())


exporter = CurlExporter()
