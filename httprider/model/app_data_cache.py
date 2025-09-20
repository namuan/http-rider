import logging

from ..core import json_path, response_code_formatter, response_code_round_up
from ..core.constants import DEFAULT_TAG, AssertionDataSource
from ..model.app_data import (
    ApiCall,
    ApiTestCase,
    AppState,
    Assertion,
    Environment,
    HttpExchange,
)
from ..model.app_data_reader import AppDataReader
from ..model.app_data_writer import AppDataWriter


def _build_filter_query(query=None, tag=None):
    selected_tag = tag if tag != DEFAULT_TAG else None
    if selected_tag and query:
        return lambda api_call: query.lower() in api_call.title.lower() and selected_tag in api_call.tags

    if selected_tag:
        return lambda api_call: selected_tag in api_call.tags

    if query:
        return lambda api_call: query.lower() in api_call.title.lower()

    return lambda api_call: api_call


class AppDataCache:
    api_call_list: dict[str, ApiCall] = {}
    api_test_cases: dict[str, ApiTestCase] = {}
    api_http_exchanges: dict[str, list[HttpExchange]] = {}
    app_state: AppState = None
    search_query = None
    environments: dict[str, Environment] = {}

    def __init__(self, data_reader: AppDataReader, data_writer: AppDataWriter):
        self.app_data_reader = data_reader
        self.app_data_writer = data_writer

        # API Calls
        self.app_data_writer.signals.api_call_added.connect(self.on_api_call_added)
        self.app_data_writer.signals.api_call_removed.connect(self.on_api_call_removed)
        self.app_data_writer.signals.multiple_api_calls_added.connect(self.on_multiple_api_calls_added)
        self.app_data_writer.signals.api_call_tag_added.connect(lambda c: self.refresh_cache_item(c.id))
        self.app_data_writer.signals.api_call_tag_removed.connect(lambda c: self.refresh_cache_item(c.id))
        self.app_data_writer.signals.api_call_updated.connect(self.refresh_cache_item)

        # AppState
        self.app_data_writer.signals.app_state_updated.connect(self.refresh_app_state)

        # API Test Cases
        self.app_data_writer.signals.api_test_case_changed.connect(self.refresh_api_test_case)

        # API Exchange
        self.app_data_writer.signals.exchange_added.connect(self.on_api_http_exchange_added)
        self.app_data_writer.signals.exchange_changed.connect(self.on_api_http_exchange_updated)

        # Environments
        self.app_data_writer.signals.environment_added.connect(self.refresh_environments)
        self.app_data_writer.signals.environment_removed.connect(self.refresh_environments)
        self.app_data_writer.signals.environment_renamed.connect(self.refresh_environments)
        self.app_data_writer.signals.environment_data_changed.connect(self.refresh_environments)

    def load_cache(self):
        self.api_call_list = self.app_data_reader.get_all_api_calls_from_db()
        for _, api_call in self.api_call_list.items():
            api_test_case = self.app_data_reader.get_api_test_case_from_db(api_call.id)
            self.api_test_cases[api_call.id] = api_test_case
            http_exchanges = self.app_data_reader.get_api_call_exchanges(api_call.id)
            self.api_http_exchanges[api_call.id] = http_exchanges

        self.refresh_app_state()
        self.refresh_environments()
        logging.info(
            f"Initial Cache Loading Completed: "
            f"API Calls: {len(self.api_call_list)} - "
            f"API Test Cases: {len(self.api_test_cases)} - "
            f"API HTTP Exchanges: {len(self.api_http_exchanges)} -"
            f"Environments: {len(self.environments)} - "
        )
        self.app_data_reader.signals.initial_cache_loading_completed.emit()

    def refresh_environments(self):
        self.environments = {e.name: e for e in self.app_data_reader.get_environments_from_db()}

    def get_environments(self):
        return self.environments.values()

    def get_selected_environment(self, environment_name):
        return self.environments.get(environment_name, Environment.from_json())

    def on_api_http_exchange_added(self, exchange):
        http_exchanges = self.api_http_exchanges.get(exchange.api_call_id, [])
        http_exchanges.append(exchange)
        self.api_http_exchanges[exchange.api_call_id] = http_exchanges

    def on_api_http_exchange_updated(self, exchange_id, exchange):
        api_call_id = exchange.api_call_id
        http_exchanges = self.app_data_reader.get_api_call_exchanges(api_call_id)
        self.api_http_exchanges[api_call_id] = http_exchanges

    def get_all_api_calls(self):
        return self.api_call_list.values()

    def get_api_call(self, api_call_id):
        return self.api_call_list.get(api_call_id)

    def refresh_api_test_case(self, api_call_id):
        api_test_case = self.app_data_reader.get_api_test_case_from_db(api_call_id)
        self.api_test_cases[api_call_id] = api_test_case

    def refresh_app_state(self):
        self.app_state = self.app_data_reader.get_app_state()

    def refresh_cache_item(self, api_call_id):
        refreshed_api_call = self.app_data_reader.get_api_call_from_db(api_call_id)
        self.api_call_list[api_call_id] = refreshed_api_call

    def on_api_call_added(self, doc_id, api_call: ApiCall):
        api_call.id = doc_id
        self.api_call_list[doc_id] = api_call

    def on_api_call_removed(self, doc_ids):
        for doc_id in doc_ids:
            if self.api_call_list.get(doc_id, None):
                del self.api_call_list[doc_id]

    def on_multiple_api_calls_added(self, doc_ids: list[str], api_calls: list[ApiCall]):
        for doc_id, api_call in zip(doc_ids, api_calls, strict=False):
            api_call.id = doc_id
            self.api_call_list[api_call.id] = api_call

    def filter_api_calls(self, search_query=None, search_tag=None):
        logging.info(f"Filtering API Calls by Query {search_query} and Tag {search_tag}")
        api_calls_filter = _build_filter_query(query=search_query, tag=search_tag)
        all_api_calls = self.get_all_api_calls()
        return sorted(
            filter(api_calls_filter, all_api_calls),
            key=lambda a: a.sequence_number or 0,
        )

    def get_all_active_api_calls(self):
        """Returns all APIs currently rendered in the List view"""
        app_state = self.get_app_state()
        return [
            api_call
            for api_call in self.filter_api_calls(
                search_query=app_state.selected_search,
                search_tag=app_state.selected_tag,
            )
            if api_call.enabled
        ]

    def update_search_query(self, search_query):
        self.search_query = search_query

    def get_all_env_variables(self):
        current_env = self.get_appstate_environment()
        environment: Environment = self.get_selected_environment(current_env)
        return [f"${{{k}}}" for k in environment.get_data()]

    def get_appstate_environment(self):
        app_state = self.get_app_state()
        return app_state.selected_env

    def get_app_state(self):
        self.app_state.selected_search = self.search_query
        return self.app_state

    @staticmethod
    def get_latest_assertion_value_from_exchange(assertion: Assertion, exchange: HttpExchange):
        if assertion.data_from == AssertionDataSource.REQUEST_HEADER.value:
            return exchange.request.headers.get(assertion.selector.lower(), None)
        elif assertion.data_from == AssertionDataSource.RESPONSE_HEADER.value:
            return exchange.response.headers.get(assertion.selector.lower(), None)
        elif assertion.data_from == AssertionDataSource.REQUEST_BODY.value:
            return json_path(exchange.request.request_body, assertion.selector)
        elif assertion.data_from == AssertionDataSource.RESPONSE_BODY.value:
            return json_path(exchange.response.response_body, assertion.selector)
        elif assertion.data_from == AssertionDataSource.RESPONSE_CODE.value:
            return response_code_formatter(exchange.response.http_status_code)
        elif assertion.data_from == AssertionDataSource.RESPONSE_TIME.value:
            return response_code_round_up(exchange.response.elapsed_time)

    def __build_assertion(self, api_call: ApiCall, exchange: HttpExchange, api_test_case: ApiTestCase):
        return {
            assertion.var_name: self.get_latest_assertion_value_from_exchange(assertion, exchange)
            for assertion in api_test_case.assertions
        }

    def get_http_exchange(self, exchange_id):
        return self.app_data_reader.get_http_exchange_from_db(exchange_id)

    def get_api_call_exchanges(self, api_call_id):
        return self.api_http_exchanges.get(api_call_id, [])

    def get_last_exchange(self, api_call_id):
        api_call_exchanges = self.get_api_call_exchanges(api_call_id)
        if api_call_exchanges:
            return api_call_exchanges[-1]
        else:
            return HttpExchange(api_call_id)

    def get_api_test_case(self, api_call_id):
        return self.api_test_cases.get(api_call_id, ApiTestCase.from_json(None, api_call_id))

    def get_multiple_api_latest_exchanges(self, api_calls: list[ApiCall]):
        """Returns latest Http Exchanges for multiple API Calls"""
        return [self.get_last_exchange(api_call.id) for api_call in api_calls]

    def get_all_api_test_assertions(self):
        api_calls = self.get_all_api_calls()
        return [
            self.__build_assertion(
                api_call,
                self.get_last_exchange(api_call.id),
                self.get_api_test_case(api_call.id),
            )
            for api_call in api_calls
        ]
