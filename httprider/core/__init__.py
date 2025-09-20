import ast
import base64
import codecs
import functools
import importlib
import json
import logging
import pkgutil
import uuid
from datetime import timedelta
from enum import Enum
from json import JSONDecodeError
from pathlib import Path
from string import Template
from urllib import parse

import attr
from jsonpath_ng.ext import parse as jsonpath_parse
from PyQt6.QtWidgets import QApplication

from .constants import UTF_8_ENCODING, ContentType
from .faker_config import fake
from .generators import internal_func_rgx, random_string_generator, return_func_result

__all__ = [
    "UTF_8_ENCODING",
    "ContentType",
    "DynamicStringData",
    "DynamicStringType",
    "abbreviate",
    "bytes_to_str",
    "combine_request_headers",
    "compact_json",
    "data_type",
    "elapsed_time_formatter",
    "evaluate_nested_functions",
    "fake",
    "flatten_variables",
    "format_json",
    "gen_uuid",
    "get_variable_tokens",
    "guess_content_type",
    "import_modules",
    "internal_func_rgx",
    "json_path",
    "kv_list_to_dict",
    "load_json_show_error",
    "mask_secret",
    "random_environment",
    "random_project_name",
    "random_string_generator",
    "replace_response_variables",
    "replace_variables",
    "response_code_formatter",
    "response_code_round_up",
    "return_func_result",
    "rot13",
    "split_url_qs",
    "str_to_base64_encoded_bytes",
    "str_to_bool",
    "str_to_bytes",
    "str_to_int",
    "strip_comments",
    "template_sub",
    "tor31",
    "truncate",
]


class DynamicStringType(Enum):
    PLAIN = "plain"
    # ruff: noqa: S105
    SECRET = "secret"


@attr.s(auto_attribs=True)
class DynamicStringData:
    # Deprecated property display_text
    display_text: str = "NOT_USED"
    value: str = ""
    string_type: str = DynamicStringType.PLAIN.value
    is_enabled: bool = True

    def display_value(self):
        return self.value if self.string_type == DynamicStringType.PLAIN.value else "*" * len(self.value)


def rot13(in_str: str):
    return codecs.encode(in_str, "rot13")


def tor31(in_str: str):
    return codecs.decode(in_str, "rot13")


def abbreviate(in_str: str, length=30):
    return f"{in_str[:length]} ..." if len(in_str) > length else in_str


def truncate(directory, with_parent=True):
    p = Path(directory)
    if with_parent:
        return f"../{p.parent.name}/{p.name}"
    return p.name


def str_to_int(int_str, default=0):
    if int_str and type(int_str) is str:
        return int(int_str)

    return default


def str_to_bool(bool_str):
    if type(bool_str) is bool:
        return bool_str
    return bool_str.lower() in ("yes", "true", "t", "1")


def kv_list_to_dict(kv_list):
    return {item["key"]: item["value"] for item in kv_list}


def random_environment():
    return fake.domain_word()


def random_project_name():
    return f"{QApplication.instance().applicationName()}-{fake.domain_word()}.tmp.db"


def elapsed_time_formatter(elapsed_time):
    if isinstance(elapsed_time, timedelta):
        total_ms = elapsed_time.total_seconds() * 1000
        return "N/A" if total_ms <= 0 else f"{total_ms:.0f} ms"
    return "N/A" if elapsed_time <= 0 else f"{elapsed_time:.0f} ms"


def response_code_formatter(response_code):
    return "N/A" if response_code <= 0 else str(response_code)


def response_code_round_up(response_code):
    i = int(response_code * 100)
    return i / 100


def data_type(val):
    try:
        norm_val = val.strip() if isinstance(val, str) else str(val)
        if len(norm_val) == 0:
            return "none"
        if norm_val in ["true", "True", "false", "False"]:
            return "bool"

        return type(ast.literal_eval(norm_val)).__name__
    except ValueError:
        return "str"
    except SyntaxError:
        return "str"


def json_path(json_doc, path_query):
    try:
        j = json.loads(json_doc)
        parsed_query = jsonpath_parse(path_query)
        key_found = parsed_query.find(j)
        if key_found:
            return key_found[0].value
        return None
    except Exception:
        logging.exception(f"json_path failed: {json_doc} path query: {path_query}")
        return None


def flatten_variables(x: dict, y: dict):
    for k, v in y.items():
        x[k] = v
    return x


def replace_response_variables(vars_tokens, exchange_response):
    for hk, hv in exchange_response.headers.items():
        exchange_response.headers[hk] = template_sub(hv, vars_tokens)

    exchange_response.response_body = template_sub(exchange_response.response_body, vars_tokens)
    return exchange_response


def combine_request_headers(app_settings, exchange_request):
    """Inject common headers respecting existing headers on the request"""
    project_info = app_settings.app_data_reader.get_or_create_project_info()
    common_headers = {k: v.value for k, v in project_info.common_headers.items()}
    return {**common_headers, **exchange_request.headers}


def get_variable_tokens(app_settings):
    active_env = app_settings.app_data_cache.get_appstate_environment()
    env = app_settings.app_data_cache.get_selected_environment(active_env)

    all_runtime_vars = app_settings.app_data_cache.get_all_api_test_assertions()
    flatten_runtime_vars = functools.reduce(flatten_variables, all_runtime_vars, {})

    env_map = env.get_env_map()
    return {**env_map, **flatten_runtime_vars}


def replace_variables(vars_tokens, exchange_request):
    exchange_request.http_url = template_sub(exchange_request.http_url, vars_tokens)
    for hk, hv in exchange_request.headers.items():
        exchange_request.headers[hk] = template_sub(hv, vars_tokens)

    for qk, qv in exchange_request.query_params.items():
        exchange_request.query_params[qk] = template_sub(qv, vars_tokens)

    for fk, fv in exchange_request.form_params.items():
        exchange_request.form_params[fk] = template_sub(fv, vars_tokens)

    exchange_request.request_body = compact_json(template_sub(exchange_request.request_body, vars_tokens))
    return exchange_request


def template_sub(templated_string, tokens):
    return evaluate_nested_functions(Template(templated_string).safe_substitute(tokens) if templated_string else "")


def evaluate_nested_functions(templated_string):
    match_found = internal_func_rgx.search(templated_string)
    while match_found:
        templated_string = internal_func_rgx.sub(return_func_result, templated_string, count=0)
        match_found = internal_func_rgx.search(templated_string)

    return templated_string


def import_modules(package):
    return {
        name: importlib.import_module(name)
        for finder, name, ispkg in pkgutil.iter_modules(package.__path__, package.__name__ + ".")
    }


def split_url_qs(url: str):
    url_qs = url.split("?", 1)
    if len(url_qs) > 1:
        qs = parse.parse_qs(url_qs[1])
        return (
            url_qs[0],
            {qk: DynamicStringData(value=",".join(qv)) for qk, qv in qs.items()},
        )
    return url_qs[0], {}


def format_json(json_str):
    if not json_str:
        return ""

    try:
        j = json.loads(json_str)
        return json.dumps(j, indent=4)
    except JSONDecodeError:
        return json_str


def compact_json(json_str):
    if not json_str:
        return ""

    try:
        j = json.loads(json_str)
        return json.dumps(j)
    except JSONDecodeError:
        return json_str


def guess_content_type(body):
    try:
        json.loads(body)
        return ContentType.JSON
    except JSONDecodeError:
        return ContentType.RAW


def load_json_show_error(json_str):
    try:
        return json.loads(json_str)
    except JSONDecodeError:
        logging.exception(f"Error in loading JSON: {json_str}")


def gen_uuid():
    return str(uuid.uuid4())


def strip_comments(request_body):
    return "".join([l for l in request_body.splitlines() if not l.lstrip().startswith("//")])


def mask_secret(str_val):
    return "*" * len(str_val)


def str_to_bytes(input_str: str):
    return bytes(input_str, encoding="utf-8")


def bytes_to_str(input_bytes: bytes):
    return input_bytes.decode(encoding="utf-8")


def str_to_base64_encoded_bytes(input_str) -> bytes:
    return base64.standard_b64encode(str_to_bytes(input_str))
