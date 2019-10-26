import json
from collections import defaultdict

import attr
import cattr
from typing import List, Any, Optional, Dict

from httprider.core import internal_func_rgx
from httprider.core.generators import call_generator_func
from ..core import gen_uuid
from ..core.constants import AssertionMatchers, AssertionDataSource
from ..core.core_settings import app_settings
from ..exporters import *
from ..model.app_data import ApiTestCase, HttpExchange, Environment, Assertion

internal_func_map = defaultdict(str)


@attr.s(auto_attribs=True)
class RunscopeEnvironment(object):
    initial_variables: Dict
    name: str
    id: str
    verify_ssl: bool


@attr.s(auto_attribs=True)
class RunscopeVariable(object):
    source: str
    property: str
    name: str


@attr.s(auto_attribs=True)
class RunscopeAssertion(object):
    comparison: str
    source: str
    value: int
    property: str


@attr.s(auto_attribs=True)
class Step(object):
    assertions: List[RunscopeAssertion]
    auth: Dict
    body: str
    form: Dict
    headers: Dict
    method: str
    note: str
    step_type: str
    url: str
    id: str
    variables: List[Any]


@attr.s(auto_attribs=True)
class RunscopeTest(object):
    name: str
    description: str
    environments: List[RunscopeEnvironment]
    steps: List[Step]
    version: str = "1.0"
    trigger_url: Optional[str] = ""

    def to_json(self):
        return cattr.unstructure(self)

    def to_raw_json(self):
        return json.dumps(self.to_json())


def to_runscope_env(env: Environment, func_map: Dict):
    return RunscopeEnvironment(
        initial_variables={**env.get_env_map(), **func_map},
        name=env.name,
        id=env.id,
        verify_ssl=True
    )


def to_runscope_matcher(matcher, assertion_var_type):
    mapper = {
        AssertionMatchers.EQ.value: "equal_number" if assertion_var_type == "int" else "equal",
        AssertionMatchers.NOT_EQ.value: "not_equal",
        AssertionMatchers.NOT_NULL.value: "not_empty",
        AssertionMatchers.EMPTY.value: "empty",
        AssertionMatchers.NOT_EMPTY.value: "not_empty",
        AssertionMatchers.CONTAINS.value: "contains",
        AssertionMatchers.NOT_CONTAINS.value: "does_not_contain",
        AssertionMatchers.LT.value: "is_less_than",
        AssertionMatchers.GT.value: "is_greater_than"
    }

    return mapper.get(matcher, None)


def to_runscope_source(data_source):
    mapper = {
        AssertionDataSource.RESPONSE_CODE.value: "response_status",
        AssertionDataSource.RESPONSE_BODY.value: "response_json"
    }

    return mapper.get(data_source, None)


def to_runscope_property(selector):
    return selector.replace("$.", "")


def to_runscope_value(expected_value):
    return expected_value


def to_runscope_assertion(assertion: Assertion):
    return RunscopeAssertion(
        comparison=to_runscope_matcher(assertion.matcher, assertion.var_type),
        source=to_runscope_source(assertion.data_from),
        property=to_runscope_property(assertion.selector),
        value=to_runscope_value(assertion.expected_value)
    )


def to_runscope_variable(assertion: Assertion):
    runscope_var = RunscopeVariable(
        property=to_runscope_property(assertion.selector),
        source=to_runscope_source(assertion.data_from),
        name=assertion.var_name
    )
    return runscope_var


def convert_internal_variable(str_with_variable):
    return internal_var_selector.sub(r"{{\1}}", str_with_variable, count=0) if str_with_variable else ""


ENV_PREFIX = "env_var"


def convert_internal_functions(str_with_internal_func):
    return internal_func_rgx.sub(r"{{{{{0}_\1}}}}".format(ENV_PREFIX), str_with_internal_func, count=0)


def find_internal_functions(str_with_internal_func):
    return internal_func_rgx.findall(str_with_internal_func)


def to_runscope_format(str_with_internal_keywords):
    """
    Using a global variable to store function map. It creates a map of variable name -> evaluated function value
    The global variable is then passed to to_runscope_env where the variables are set as initial variables
    :param str_with_internal_keywords: It could be URL, Header/Query param value or the request body
    :return: string with the internal keywords replaced by runscope syntax
    """
    global internal_func_map
    func_map = {
        f"{ENV_PREFIX}_{k[0]}": call_generator_func(k[0], k[1])
        for k in find_internal_functions(str_with_internal_keywords)
    }
    internal_func_map = {**internal_func_map, **func_map}
    return convert_internal_functions(convert_internal_variable(str_with_internal_keywords))


def to_runscope_request_body(request_body):
    return to_runscope_format(request_body)


def to_runscope_url(api_call):
    """Build URL from ApiCall combing with query parameters
    """
    req_qp = api_call.enabled_query_params()
    http_url = api_call.http_url
    if req_qp:
        http_url = api_call.http_url + "?" + "&".join([f"{k}={v}" for k, v in req_qp.items()])
    return to_runscope_format(http_url)


def to_runscope_step(
        api_call: ApiCall,
        last_exchange: HttpExchange,
        api_test_case: ApiTestCase):
    transformed_request_body = to_runscope_request_body(api_call.http_request_body)
    return Step(
        assertions=[to_runscope_assertion(a) for a in api_test_case.comparable_assertions()],
        auth={},
        body=transformed_request_body,
        form={k: to_runscope_format(v) for k, v in api_call.enabled_form_params().items()},
        headers={k: to_runscope_format(v) for k, v in api_call.enabled_headers().items()},
        method=last_exchange.request.http_method,
        note=api_call.title,
        step_type="request",
        url=to_runscope_url(api_call),
        id=gen_uuid(),
        variables=[to_runscope_variable(a) for a in api_test_case.variables()]
    )


class RunscopeExporter:
    name: str = "Runscope"
    output_ext: str = "json"

    def export_data(self, api_calls: List[ApiCall]):
        project_info = app_settings.app_data_reader.get_or_create_project_info()
        environments = app_settings.app_data_cache.get_environments()

        output_steps = [
            self.__export_api_call(api_call)
            for api_call in api_calls
        ]

        runscope_test = RunscopeTest(
            name=project_info.title,
            description=project_info.info,
            environments=[to_runscope_env(env, internal_func_map) for env in environments],
            steps=output_steps
        )

        return highlight_format_json(runscope_test.to_raw_json())

    def __export_api_call(self, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        api_test_case = app_settings.app_data_cache.get_api_test_case(api_call.id)
        return to_runscope_step(api_call, last_exchange, api_test_case)


exporter = RunscopeExporter()
