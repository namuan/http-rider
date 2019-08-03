from datetime import datetime, timedelta

import attr
import cattr
from requests.structures import CaseInsensitiveDict
from typing import Any, Optional, Dict, List

from ..core import DynamicStringData, strip_comments
from ..core.constants import *


@attr.s(auto_attribs=True)
class TagInfo(object):
    name: str = ""
    description: str = ""


@attr.s(auto_attribs=True)
class ProjectInfo(object):
    record_type: str = PROJECT_INFO_RECORD_TYPE
    id: str = ""
    title: str = ""
    version: str = ""
    tos_url: str = ""
    contact_name: str = ""
    contact_email: str = ""
    info: str = ""
    license_url: str = ""
    license_name: str = ""
    setup_code: str = ""
    teardown_code: str = ""
    tags: List[TagInfo] = []
    servers: List[str] = []
    common_headers: Dict[str, DynamicStringData] = {}

    @classmethod
    def from_json(cls, json_obj):
        if not json_obj:
            return cls()
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)


@attr.s(auto_attribs=True)
class AppState(object):
    record_type: str = APP_STATE_RECORD_TYPE
    selected_tag: Optional[str] = None
    selected_env: Optional[str] = None
    selected_search: Optional[str] = None
    last_sequence_number: Optional[int] = 0

    @classmethod
    def from_json(cls, json_obj=None):
        if not json_obj:
            return cls()
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)


@attr.s(auto_attribs=True)
class MockedResponse(object):
    is_enabled: bool = False
    status_code: int = 200
    headers: Dict[str, DynamicStringData] = {}
    body: str = ""


@attr.s(auto_attribs=True)
class ApiCall(object):
    id: str = None
    description: str = ""
    title: str = ""
    http_url: str = ""
    http_method: str = ""
    http_headers: Dict[str, DynamicStringData] = {}
    http_params: Dict[str, DynamicStringData] = {}
    form_params: Dict[str, DynamicStringData] = {}
    http_request_body: str = ""
    sequence_number: Optional[int] = None
    type: str = API_CALL_RECORD_TYPE
    tags: List = []
    last_response_code: Optional[int] = None
    enabled: bool = True
    last_assertion_result: Optional[bool] = None
    mocked_response: MockedResponse = MockedResponse()
    is_separator: bool = False

    @classmethod
    def from_json(cls, json_obj=None):
        if not json_obj:
            return cls()
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)


@attr.s(auto_attribs=True)
class ExchangeRequest(object):
    request_time: str = ""
    http_method: str = "GET"
    http_url: str = "Request not available"
    headers: Dict = {}
    query_params: Dict = {}
    form_params: Dict = {}
    request_body: str = ""
    request_body_type: ContentType = ContentType.NONE

    def content_type(self):
        return self.headers.get("Content-Type", self.request_body_type.value)

    @classmethod
    def from_api_call(cls, api_call: ApiCall):
        return cls(
            request_time=datetime.now().strftime("%c"),
            http_method=api_call.http_method,
            http_url=api_call.http_url,
            headers={k: v.display_text for k, v in api_call.http_headers.items() if v.is_enabled},
            query_params={k: v.display_text for k, v in api_call.http_params.items() if v.is_enabled},
            form_params={k: v.display_text for k, v in api_call.form_params.items() if v.is_enabled},
            request_body=strip_comments(api_call.http_request_body)
        )


@attr.s(auto_attribs=True)
class ExchangeResponse(object):
    http_status_code: int = 0
    response_headers: Dict = {}
    response_body: str = ""
    response_body_type: ContentType = ContentType.NONE
    response_time: float = 0.0
    is_mocked: bool = False

    @property
    def elapsed_time(self):
        return self.response_time

    @elapsed_time.setter
    def elapsed_time(self, new_value: timedelta):
        self.response_time = new_value.total_seconds() * 1000

    @property
    def headers(self):
        return self.response_headers

    @headers.setter
    def headers(self, new_headers: CaseInsensitiveDict):
        self.response_headers = {k: v for k, v in new_headers.lower_items()}

    def content_type(self):
        return self.headers.get("Content-Type", self.response_body_type.value)

    @classmethod
    def from_mocked_response(cls, mocked_response: MockedResponse):
        return cls(
            response_headers={k: v.display_text for k, v in mocked_response.headers.items() if v.is_enabled},
            response_body=mocked_response.body,
            http_status_code=mocked_response.status_code,
            is_mocked=True,
            response_time=0.0
        )


@attr.s(auto_attribs=True)
class Assertion(object):
    data_from: str = None
    var_name: str = None
    selector: str = None
    matcher: str = None
    expected_value: Any = None
    output: str = None
    var_type: str = None
    result: Optional[bool] = None


@attr.s(auto_attribs=True)
class HttpExchange(object):
    api_call_id: str
    id: str = None
    request: ExchangeRequest = ExchangeRequest()
    type: str = HTTP_EXCHANGE_RECORD_TYPE
    response: ExchangeResponse = ExchangeResponse()
    assertions: List[Assertion] = []

    @classmethod
    def from_json(cls, json_obj, api_call_id=None):
        if not json_obj:
            return cls(api_call_id)
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)


@attr.s(auto_attribs=True)
class Environment(object):
    id: str = None
    record_type: str = ENVIRONMENT_RECORD_TYPE
    name: str = None
    data: Dict[str, DynamicStringData] = {}

    @classmethod
    def from_json(cls, json_obj=None):
        if not json_obj:
            return cls()
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)

    def add_data(self, k, v):
        self.data[k] = DynamicStringData(display_text=v)

    def set_data(self, new_data):
        self.data = new_data

    def get_data(self):
        return self.data


@attr.s(auto_attribs=True)
class ApiTestCase(object):
    api_call_id: str
    id: str = None
    record_type: str = API_TEST_CASE_RECORD_TYPE
    assertions: List[Assertion] = []

    def to_json(self):
        return cattr.unstructure(self)

    @classmethod
    def from_json(cls, json_obj, api_call_id):
        if not json_obj:
            return cls(api_call_id=api_call_id)

        return cattr.structure(json_obj, cls)


class AppData:
    ldb = None
