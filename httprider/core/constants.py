from enum import Enum

from PyQt5.QtCore import Qt

ENVIRONMENT_RECORD_TYPE = "environment"
PROJECT_INFO_RECORD_TYPE = "project_info"
APP_STATE_RECORD_TYPE = "app_state"
HTTP_EXCHANGE_RECORD_TYPE = "http_exchange"
API_TEST_CASE_RECORD_TYPE = "api_test"
API_CALL_RECORD_TYPE = "api"
DEFAULT_TAG = "Show All"

API_CALL_ROLE = Qt.UserRole + 100
API_ID_ROLE = API_CALL_ROLE + 100
ASSERTION_TYPE_ROLE = Qt.UserRole + 300
DYNAMIC_STRING_ROLE = Qt.UserRole + 400
EXPORTER_COMBO_ROLE = Qt.UserRole + 500

UTF_8_ENCODING = 'utf-8'


class AssertionDataSource(Enum):
    REQUEST_HEADER = "request_header"
    RESPONSE_HEADER = "response_header"
    REQUEST_BODY = "request_body"
    RESPONSE_BODY = "response_body"
    RESPONSE_CODE = "response_code"
    RESPONSE_TIME = "response_time"


class AssertionOutput(Enum):
    PASSED = "passed"
    FAILED = "failed"


class AssertionMatchers(Enum):
    SKIP = "---"
    EQ = "equalTo"
    NOT_EQ = "notEqualTo"
    NOT_NULL = "notNull"
    EMPTY = "isEmpty"
    NOT_EMPTY = "isNotEmpty"
    CONTAINS = "containsString"
    NOT_CONTAINS = "notContainsString"
    LT = "lessThan"
    GT = "greaterThan"


HTTP_CONTENT_TYPES = [
    'application/json',
    'application/x-www-form-urlencoded',
    'multipart/form-data',
    'application/octet-stream',
    'application/pdf',
    'application/xml'
]

COMMON_HEADERS = [
    "Content-Type",
    "Accept",
    "Authorization"
]


class ContentType(Enum):
    NONE = ""
    RAW = "text/plain"
    XML = "application/xml"
    JSON = "application/json"
    FORM = "application/x-www-form-urlencoded"


REPLACEMENTS = [
    ('-', '_'),
    (' ', '_'),
    ('[', ''),
    (']', ''),
    ('$', ''),
    ('.', '_')
]
