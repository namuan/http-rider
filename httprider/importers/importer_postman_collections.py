import json
import re
from pathlib import Path

import attr
import cattr
from typing import Dict, List

from ..core import kv_list_to_dict, DynamicStringData
from ..core.core_settings import app_settings
from ..model.app_data import ApiCall


@attr.s(auto_attribs=True)
class PostmanRequest:
    method: str
    header: List = []
    body: Dict = {}
    url: Dict = {}


@attr.s(auto_attribs=True)
class PostmanSubItem:
    name: str
    request: PostmanRequest
    response: List
    event: List = []


@attr.s(auto_attribs=True)
class PostmanItem:
    name: str
    item: List[PostmanSubItem]
    event: List = []


@attr.s(auto_attribs=True)
class PostmanDataModel:
    info: Dict
    item: List[PostmanItem]


@attr.s
class PostmanCollectionImporter:
    name: str = "Postman Collections v2"
    input_type: str = "file"
    var_selector = r"({{(\w+)}})+"

    def import_data(self, file_path):
        self.__validate_file(file_path)
        json_data = json.loads(Path(file_path).read_text())
        postman_data: PostmanDataModel = cattr.structure(json_data, PostmanDataModel)
        return None, [
            self.__extract_api_call(item, sub_item)
            for item in postman_data.item
            for sub_item in item.item
        ]

    def __extract_api_call(self, item: PostmanItem, sub_item: PostmanSubItem):
        api_call = ApiCall(
            tags=[item.name],
            title=sub_item.name,
            description=sub_item.name,
            http_url=self.__internal_variables(sub_item.request.url.get('raw')),
            http_method=sub_item.request.method,
            http_request_body=self.__internal_variables(sub_item.request.body.get('raw')),
            http_headers={
                k: DynamicStringData(display_text=self.__internal_variables(v))
                for k, v in kv_list_to_dict(sub_item.request.header).items()
            },
            sequence_number=app_settings.app_data_writer.generate_sequence_number()

        )
        return api_call

    def __internal_variables(self, input_str):
        return re.sub(self.var_selector, r"${\2}", input_str, count=0)

    def __validate_file(self, file_path):
        if not (Path(file_path).exists() and Path(file_path).is_file()):
            raise FileNotFoundError(f"Path {file_path} should be a valid file path")


importer = PostmanCollectionImporter()
