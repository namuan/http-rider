from datetime import datetime, timedelta
from typing import Any

import attr
import cattr
from requests.structures import CaseInsensitiveDict

from httprider.core import DynamicStringData, compact_json, strip_comments
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
    tags: list[TagInfo] = []
    servers: list[str] = []
    common_headers: dict[str, DynamicStringData] = {}

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
    headers: dict[str, DynamicStringData] = {}
    body: str = ""


@attr.s(auto_attribs=True)
class ApiCall:
    id: str = None
    description: str = ""
    title: str = ""
    http_url: str = ""
    http_method: str = ""
    http_headers: dict[str, DynamicStringData] = {}
    http_params: dict[str, DynamicStringData] = {}
    form_params: dict[str, DynamicStringData] = {}
    http_request_body: str = ""
    sequence_number: int | None = None
    type: str = API_CALL_RECORD_TYPE
    tags: list = []
    last_response_code: int | None = None
    enabled: bool = True
    last_assertion_result: bool | None = None
    mocked_response: MockedResponse = MockedResponse()
    is_separator: bool = False

    @classmethod
    def from_json(cls, json_obj=None):
        if not json_obj:
            return cls()
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)

    def enabled_headers(self, hide_secrets=True):
        return {
            k.lower(): v.display_value() if hide_secrets else v.value
            for k, v in self.http_headers.items()
            if v.is_enabled
        }

    def enabled_query_params(self, hide_secrets=True):
        return {k: v.display_value() if hide_secrets else v.value for k, v in self.http_params.items() if v.is_enabled}

    def enabled_form_params(self, hide_secrets=True):
        return {k: v.display_value() if hide_secrets else v.value for k, v in self.form_params.items() if v.is_enabled}

    def request_body_without_comments(self):
        return compact_json(strip_comments(self.http_request_body))


@attr.s(auto_attribs=True)
class ExchangeRequest:
    request_time: str = ""
    http_method: str = "GET"
    http_url: str = "Request not available"
    full_encoded_url: str = "Request not available"
    headers: dict = {}
    query_params: dict = {}
    form_params: dict = {}
    request_body: str = ""
    request_body_type: ContentType = ContentType.NONE
    request_type: ExchangeRequestType = ExchangeRequestType.NORMAL

    def content_type(self):
        return self.headers.get(CONTENT_TYPE_HEADER_IN_EXCHANGE, self.request_body_type.value)

    def is_fuzzed(self):
        return self.request_type and self.request_type.value == ExchangeRequestType.FUZZED.value

    def url_with_qp(self):
        if self.query_params:
            return self.http_url + "?" + "&".join([f"{k}={v}" for k, v in self.query_params.items()])
        else:
            return self.http_url

    @classmethod
    def from_api_call(cls, api_call: ApiCall, hide_secrets=True):
        return cls(
            request_time=datetime.now().strftime("%c"),
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
    response_headers: dict = {}
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
        return self.headers.get(CONTENT_TYPE_HEADER_IN_EXCHANGE, self.response_body_type.value)

    @classmethod
    def from_mocked_response(cls, mocked_response: MockedResponse):
        return cls(
            response_headers={k: v.value for k, v in mocked_response.headers.items() if v.is_enabled},
            response_body=mocked_response.body,
            http_status_code=mocked_response.status_code,
            is_mocked=True,
            response_time=0.0,
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
    request: ExchangeRequest = ExchangeRequest()
    type: str = HTTP_EXCHANGE_RECORD_TYPE
    response: ExchangeResponse = ExchangeResponse()
    response_status: ExchangeResponseStatus = ExchangeResponseStatus.NONE
    assertions: list[Assertion] = []

    def is_passed(self):
        return self.response_status == ExchangeResponseStatus.PASSED

    def is_failed(self):
        return not self.is_passed()

    def passed(self):
        self.response_status = ExchangeResponseStatus.PASSED

    def failed(self):
        self.response_status = ExchangeResponseStatus.FAILED

    @classmethod
    def from_json(cls, json_obj, api_call_id=None):
        if not json_obj:
            return cls(api_call_id)
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)


@attr.s(auto_attribs=True)
class Environment:
    id: str = None
    record_type: str = ENVIRONMENT_RECORD_TYPE
    name: str = None
    data: dict[str, DynamicStringData] = {}

    @classmethod
    def from_json(cls, json_obj=None):
        if not json_obj:
            return cls()
        return cattr.structure(json_obj, cls)

    def to_json(self):
        return cattr.unstructure(self)

    def add_data(self, k, v):
        self.data[k] = DynamicStringData(value=v)

    def set_data(self, new_data):
        self.data = new_data

    def get_data(self):
        return self.data

    def get_env_map(self):
        return {k: v.value for k, v in self.get_data().items()}


@attr.s(auto_attribs=True)
class ApiTestCase:
    api_call_id: str
    id: str = None
    record_type: str = API_TEST_CASE_RECORD_TYPE
    assertions: list[Assertion] = []
    DEFAULT_VAR_PREFIX = "var"

    def to_json(self):
        return cattr.unstructure(self)

    @classmethod
    def from_json(cls, json_obj, api_call_id):
        if not json_obj:
            return cls(api_call_id=api_call_id)

        return cattr.structure(json_obj, cls)

    def comparable_assertions(self):
        return [a for a in self.assertions if a.matcher != AssertionMatchers.SKIP.value]

    def variables(self):
        return [a for a in self.assertions if not a.var_name.startswith(self.DEFAULT_VAR_PREFIX)]


class AppData:
    ldb = None
