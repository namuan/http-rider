from datetime import timedelta
from typing import Any

import attr
import cattr
from requests.structures import CaseInsensitiveDict

from httprider.core import DynamicStringData, strip_comments
from httprider.core.constants import *


@attr.s(auto_attribs=True)
class TagInfo:
    name: str = ""
    description: str = ""


@attr.s(auto_attribs=True)
class ProjectInfo:
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
    tags: list[TagInfo] = attr.Factory(list)
    servers: list[str] = attr.Factory(list)
    common_headers: dict[str, DynamicStringData] = attr.Factory(dict)

    @classmethod
    def from_json(cls, json_obj):
        if not json_obj:
            return cls()
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)


@attr.s(auto_attribs=True)
class AppState:
    record_type: str = APP_STATE_RECORD_TYPE
    selected_tag: str | None = None
    selected_env: str | None = None
    selected_search: str | None = None
    last_sequence_number: int | None = 0

    @classmethod
    def from_json(cls, json_obj=None):
        if not json_obj:
            return cls()
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)


@attr.s(auto_attribs=True)
class MockedResponse:
    is_enabled: bool = False
    status_code: int = 200
    headers: dict[str, DynamicStringData] = attr.Factory(dict)
    body: str = ""


@attr.s(auto_attribs=True)
class ApiCall:
    id: str = None
    description: str = ""
    title: str = ""
    http_url: str = ""
    http_method: str = ""
    http_headers: dict[str, DynamicStringData] = attr.Factory(dict)
    http_params: dict[str, DynamicStringData] = attr.Factory(dict)
    form_params: dict[str, DynamicStringData] = attr.Factory(dict)
    http_request_body: str = ""
    sequence_number: int | None = None
    type: str = API_CALL_RECORD_TYPE
    tags: list = attr.Factory(list)
    last_response_code: int | None = None
    enabled: bool = True
    last_assertion_result: bool | None = None
    mocked_response: MockedResponse = attr.Factory(MockedResponse)
    is_separator: bool = False

    @classmethod
    def from_json(cls, json_obj=None):
        if not json_obj:
            return cls()
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)

    def enabled_headers(self, hide_secrets=True):
        return {k: v.display_value() if hide_secrets else v.value for k, v in self.http_headers.items() if v.is_enabled}

    def enabled_query_params(self, hide_secrets=True):
        return {k: v.display_value() if hide_secrets else v.value for k, v in self.http_params.items() if v.is_enabled}

    def enabled_form_params(self, hide_secrets=True):
        return {k: v.display_value() if hide_secrets else v.value for k, v in self.form_params.items() if v.is_enabled}

    def request_body_without_comments(self):
        return strip_comments(self.http_request_body)


@attr.s(auto_attribs=True)
class ExchangeRequest:
    request_time: str = ""
    http_method: str = "GET"
    http_url: str = "Request not available"
    full_encoded_url: str = "Request not available"
    headers: dict = attr.Factory(dict)
    query_params: dict = attr.Factory(dict)
    form_params: dict = attr.Factory(dict)
    request_body: str = ""
    request_body_type: ContentType = ContentType.NONE
    request_type: ExchangeRequestType = ExchangeRequestType.NORMAL

    def content_type(self):
        return self.headers.get("Content-Type", "")

    def is_fuzzed(self):
        return self.request_type == ExchangeRequestType.FUZZED

    def url_with_qp(self):
        if self.query_params:
            return f"{self.http_url}?{self.query_params}"
        else:
            return self.http_url

    @classmethod
    def from_api_call(cls, api_call: ApiCall, hide_secrets=True):
        return cls(
            http_method=api_call.http_method,
            http_url=api_call.http_url,
            headers=api_call.enabled_headers(hide_secrets),
            query_params=api_call.enabled_query_params(hide_secrets),
            form_params=api_call.enabled_form_params(hide_secrets),
            request_body=api_call.request_body_without_comments(),
        )


@attr.s(auto_attribs=True)
class ExchangeResponse:
    http_status_code: int = 0
    response_headers: dict = attr.Factory(dict)
    response_body: str = ""
    response_body_type: ContentType = ContentType.NONE
    response_time: float = 0.0
    is_mocked: bool = False

    @property
    def elapsed_time(self):
        return timedelta(seconds=self.response_time)

    @elapsed_time.setter
    def elapsed_time(self, new_value: timedelta):
        self.response_time = new_value.total_seconds()

    @property
    def headers(self):
        return CaseInsensitiveDict(self.response_headers)

    @headers.setter
    def headers(self, new_headers: CaseInsensitiveDict):
        self.response_headers = dict(new_headers)

    def content_type(self):
        return self.headers.get("Content-Type", "")

    @classmethod
    def from_mocked_response(cls, mocked_response: MockedResponse):
        return cls(
            http_status_code=mocked_response.status_code,
            response_headers={k: v.value for k, v in mocked_response.headers.items() if v.is_enabled},
            response_body=mocked_response.body,
            is_mocked=True,
        )


@attr.s(auto_attribs=True)
class Assertion:
    data_from: str = None
    var_name: str = None
    selector: str = None
    matcher: str = None
    expected_value: Any = None
    output: str = None
    var_type: str = None
    result: bool | None = None


@attr.s(auto_attribs=True)
class HttpExchange:
    api_call_id: str
    id: str = None
    request: ExchangeRequest = attr.Factory(ExchangeRequest)
    type: str = HTTP_EXCHANGE_RECORD_TYPE
    response: ExchangeResponse = attr.Factory(ExchangeResponse)
    response_status: ExchangeResponseStatus = ExchangeResponseStatus.NONE
    assertions: list[Assertion] = attr.Factory(list)

    def is_passed(self):
        return self.response_status == ExchangeResponseStatus.PASSED

    def is_failed(self):
        return self.response_status == ExchangeResponseStatus.FAILED

    def passed(self):
        self.response_status = ExchangeResponseStatus.PASSED

    def failed(self):
        self.response_status = ExchangeResponseStatus.FAILED

    @classmethod
    def from_json(cls, json_obj, api_call_id=None):
        if not json_obj:
            return cls(api_call_id=api_call_id)
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)


@attr.s(auto_attribs=True)
class Environment:
    id: str = None
    record_type: str = ENVIRONMENT_RECORD_TYPE
    name: str = None
    data: dict[str, DynamicStringData] = attr.Factory(dict)

    @classmethod
    def from_json(cls, json_obj=None):
        if not json_obj:
            return cls()
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)

    def add_data(self, k, v):
        self.data[k] = v

    def set_data(self, new_data):
        self.data = new_data

    def get_data(self):
        return self.data

    def get_env_map(self):
        return {k: v.value for k, v in self.data.items() if v.is_enabled}


@attr.s(auto_attribs=True)
class ApiTestCase:
    api_call_id: str
    id: str = None
    record_type: str = API_TEST_CASE_RECORD_TYPE
    assertions: list[Assertion] = attr.Factory(list)
    DEFAULT_VAR_PREFIX = "var"

    def to_json(self):
        return cattr.unstructure(self)

    @classmethod
    def from_json(cls, json_obj, api_call_id):
        if not json_obj:
            return cls(api_call_id=api_call_id)
        return cattr.structure(json_obj, cls)

    def comparable_assertions(self):
        return [a for a in self.assertions if a.matcher != "extract"]

    def variables(self):
        return [a for a in self.assertions if a.matcher == "extract"]


class AppData:
    ldb = None
