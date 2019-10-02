import json

import attr
import cattr
from typing import List, Any, Optional, Dict

from httprider.core import gen_uuid
from httprider.core.constants import AssertionMatchers, AssertionDataSource
from ..core.core_settings import app_settings
from ..exporters import *
from ..model.app_data import ApiTestCase, HttpExchange, Environment, Assertion


@attr.s(auto_attribs=True)
class CreatedBy(object):
    email: str
    name: str
    id: str


@attr.s(auto_attribs=True)
class Integration(object):
    description: str
    integration_type: str
    id: str


@attr.s(auto_attribs=True)
class RunscopeEnvironment(object):
    initial_variables: Dict
    integrations: List[Integration]
    name: str
    parent_environment_id: None
    preserve_cookies: bool
    regions: List[str]
    remote_agents: List[str]
    script: str
    test_id: str
    id: str
    verify_ssl: bool
    webhooks: None


@attr.s(auto_attribs=True)
class RunscopeAssertion(object):
    comparison: str
    source: str
    value: int


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
class Data(object):
    id: str
    name: str
    description: str
    environments: List[RunscopeEnvironment]
    schedules: List[Any]
    steps: List[Step]
    created_at: Optional[int] = None
    created_by: Optional[CreatedBy] = None
    default_environment_id: Optional[str] = ""
    trigger_url: Optional[str] = ""
    last_run: Optional[int] = None


@attr.s(auto_attribs=True)
class Meta(object):
    status: str


@attr.s(auto_attribs=True)
class RunscopeTest(object):
    data: List[Data]
    error: None
    meta: Meta

    def to_json(self):
        return cattr.unstructure(self)

    def to_raw_json(self):
        return json.dumps(self.to_json())


def to_runscope_env(env: Environment):
    return RunscopeEnvironment(
        initial_variables=env.get_env_map(),
        integrations=[],
        name=env.name,
        parent_environment_id=None,
        preserve_cookies=False,
        regions=[],
        remote_agents=[],
        script="",
        test_id="",
        id=env.id,
        verify_ssl=True,
        webhooks=None
    )


def to_runscope_matcher(matcher):
    mapper = {
        AssertionMatchers.EQ.value: "is_equal"
    }

    return mapper.get(matcher, None)


def to_runscope_source(data_source):
    mapper = {
        AssertionDataSource.RESPONSE_CODE.value: "response_status"
    }

    return mapper.get(data_source, None)


def to_runscope_assertion(assertion: Assertion):
    return RunscopeAssertion(
        comparison=to_runscope_matcher(assertion.matcher),
        source=to_runscope_source(assertion.data_from),
        value=assertion.expected_value
    )


def to_runscope_step(
        api_call: ApiCall,
        last_exchange: HttpExchange,
        api_test_case: ApiTestCase):
    return Step(
        assertions=[to_runscope_assertion(a) for a in api_test_case.assertions],
        auth={},
        body=last_exchange.request.request_body,
        form=last_exchange.request.form_params,
        headers=last_exchange.request.headers,
        method=last_exchange.request.http_method,
        note=api_call.title,
        step_type="request",
        url=last_exchange.request.http_url,
        id=gen_uuid(),
        variables={}
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

        runscope_data = Data(
            id=gen_uuid(),
            name=project_info.title,
            description=project_info.info,
            environments=[to_runscope_env(env) for env in environments],
            schedules=[],
            steps=output_steps
        )

        runscope_test = RunscopeTest(
            data=[runscope_data],
            error=None,
            meta=Meta(
                status="success"
            )
        )

        return highlight_format_json(runscope_test.to_raw_json())

    def __export_api_call(self, api_call):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        api_test_case = app_settings.app_data_cache.get_api_test_case(api_call.id)
        return to_runscope_step(api_call, last_exchange, api_test_case)


exporter = RunscopeExporter()
