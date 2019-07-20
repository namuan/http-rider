import logging
from typing import List

import cattr
from PyQt5.QtCore import QObject, pyqtSignal
from tinydb import Query

from httprider.core.constants import PROJECT_INFO_RECORD_TYPE, APP_STATE_RECORD_TYPE, ENVIRONMENT_RECORD_TYPE, \
    API_TEST_CASE_RECORD_TYPE
from httprider.model import HttpExchange, ApiCall
from httprider.model.app_data import ProjectInfo, AppData, AppState, Environment, ApiTestCase


class AppDataSignals(QObject):
    exchange_added = pyqtSignal(int, HttpExchange)
    exchange_changed = pyqtSignal(int, HttpExchange)
    api_call_added = pyqtSignal(int, ApiCall)
    api_call_removed = pyqtSignal(list)
    api_call_updated = pyqtSignal(int, ApiCall)
    multiple_api_calls_added = pyqtSignal(list, list)
    selected_tag_changed = pyqtSignal(str)
    selected_env_changed = pyqtSignal(str)
    api_call_tag_added = pyqtSignal(ApiCall, str)
    api_call_tag_removed = pyqtSignal(ApiCall, str)
    environment_added = pyqtSignal(int)
    environment_removed = pyqtSignal(int)
    environment_renamed = pyqtSignal(int)
    environment_data_changed = pyqtSignal(int)
    api_test_case_changed = pyqtSignal(int)
    selected_exchange_changed = pyqtSignal(HttpExchange)
    project_info_updated = pyqtSignal(ProjectInfo)
    app_state_updated = pyqtSignal()


class AppDataWriter(AppData):

    def __init__(self, db_table):
        self.db = db_table
        self.signals = AppDataSignals()
        self.selected_api_call = None

    def add_http_exchange(self, exchange: HttpExchange):
        exchange_doc_id = self.db.insert(exchange.to_json())
        logging.info(f"API {exchange.api_call_id} - Added http exchange {exchange_doc_id}")
        exchange.id = exchange_doc_id
        self.signals.exchange_added.emit(exchange.api_call_id, exchange)
        return exchange_doc_id

    def update_http_exchange(self, exchange: HttpExchange):
        logging.info(f"API {exchange.api_call_id} - Updating http exchange {exchange}")
        self.db.update(exchange.to_json(), doc_ids=[exchange.id])
        self.signals.exchange_changed.emit(exchange.id, exchange)

    def add_api_call(self, api_call: ApiCall) -> str:
        doc_id = self.db.insert(api_call.to_json())
        self.signals.api_call_added.emit(doc_id, api_call)
        logging.info(f"API {doc_id} - Adding new API {api_call}")
        return doc_id

    def add_multiple_api_calls(self, api_calls: List[ApiCall]) -> List[str]:
        if not api_calls:
            return

        doc_ids = self.db.insert_multiple(
            [api_call.to_json() for api_call in api_calls]
        )
        self.signals.multiple_api_calls_added.emit(doc_ids, api_calls)
        return doc_ids

    def remove_api_call(self, doc_ids):
        logging.info(f"Removing API Call with Id: {doc_ids}")
        self.db.remove(doc_ids=doc_ids)
        self.signals.api_call_removed.emit(doc_ids)

    def update_api_call(self, doc_id, api_call):
        logging.info(f"API : {doc_id} - Updating API Call {api_call}")
        self.db.update(api_call.to_json(), doc_ids=[doc_id])
        self.signals.api_call_updated.emit(api_call.id, api_call)

    def update_project_info(self, project_info):
        if not project_info:
            return

        logging.info(f"Updating Project info {project_info}")
        ProjectInfoQuery = Query()
        self.db.upsert(
            project_info.to_json(),
            ProjectInfoQuery.record_type == PROJECT_INFO_RECORD_TYPE
        )
        self.signals.project_info_updated.emit(project_info)

    def update_selected_tag(self, new_tag_name):
        logging.info(f"Selected tag changed to {new_tag_name}")
        AppStateQuery = Query()
        app_state_json = self.db.get(AppStateQuery.record_type == APP_STATE_RECORD_TYPE)
        app_state = AppState.from_json(app_state_json)
        app_state.selected_tag = new_tag_name
        self.db.upsert(app_state.to_json(), AppStateQuery.record_type == APP_STATE_RECORD_TYPE)
        # @important: For now the sequence of following events are important
        # As we first update the cache in the first event which is then used in the second event handler
        self.signals.app_state_updated.emit()
        self.signals.selected_tag_changed.emit(new_tag_name)

    def generate_sequence_number(self):
        AppStateQuery = Query()
        app_state_json = self.db.get(AppStateQuery.record_type == APP_STATE_RECORD_TYPE)
        app_state = AppState.from_json(app_state_json)
        app_state.last_sequence_number = app_state.last_sequence_number + 1000
        self.db.upsert(app_state.to_json(), AppStateQuery.record_type == APP_STATE_RECORD_TYPE)
        logging.info(f"Generated new sequence number: {app_state.last_sequence_number}")
        return app_state.last_sequence_number

    def add_tag_to_api_call(self, api_call: ApiCall, new_tag_name: str):
        logging.info(f"API : {api_call.id} - Adding tag {new_tag_name}")
        api_call.tags.append(new_tag_name)
        self.db.update(api_call.to_json(), doc_ids=[api_call.id])
        self.signals.api_call_tag_added.emit(api_call, new_tag_name)

    def remove_tag_from_api_call(self, api_call: ApiCall, tag_name: str):
        logging.info(f"API: {api_call.id} - Removing tag {tag_name}")
        api_call.tags.remove(tag_name)
        self.db.update(api_call.to_json(), doc_ids=[api_call.id])
        self.signals.api_call_tag_removed.emit(api_call, tag_name)

    def rename_tag_in_api_call(self, api_call: ApiCall, old_tag_name, new_tag_name):
        logging.info(f"API: {api_call.id} - Renaming tag {old_tag_name} to {new_tag_name}")
        api_call.tags.remove(old_tag_name)
        api_call.tags.append(new_tag_name)
        self.db.update(api_call.to_json(), doc_ids=[api_call.id])
        self.signals.api_call_tag_added.emit(api_call, new_tag_name)

    def add_environment(self, environment: Environment) -> str:
        env_id = self.db.insert(environment.to_json())
        environment.id = env_id
        self.signals.environment_added.emit(env_id)
        logging.info(f"Environment {env_id} - Adding new Environment {environment}")
        return env_id

    def remove_environment(self, environment_name):
        query = Query()
        removed_doc_id = self.db.remove(
            (query.record_type == ENVIRONMENT_RECORD_TYPE) & (query.name == environment_name)
        )
        logging.info(f"Environment {removed_doc_id} - Removing environment {environment_name}")
        self.signals.environment_removed.emit(removed_doc_id)

    def update_environment_name(self, old_environment_name, new_environment_name):
        query = Query()
        updated_doc_id = self.db.update(
            set('name', new_environment_name),
            (query.record_type == ENVIRONMENT_RECORD_TYPE) & (query.name == old_environment_name)
        )
        logging.info(f"Environment {updated_doc_id} - "
                     f"Renamed environment {old_environment_name} to {new_environment_name}")
        self.signals.environment_renamed.emit(updated_doc_id)

    def update_environment_data(self, environment_name, environment_data):
        query = Query()
        updated_doc_id = self.db.update(
            set('data', cattr.unstructure(environment_data)),
            (query.record_type == ENVIRONMENT_RECORD_TYPE) & (query.name == environment_name)
        )
        logging.info(f"Environment {updated_doc_id} - "
                     f"Updated environment data for {environment_name}")
        self.signals.environment_data_changed.emit(updated_doc_id)

    def update_selected_environment(self, environment_name):
        logging.info(f"Selected environment changed to {environment_name}")
        AppStateQuery = Query()
        app_state_json = self.db.get(AppStateQuery.record_type == APP_STATE_RECORD_TYPE)
        app_state = AppState.from_json(app_state_json)
        app_state.selected_env = environment_name
        self.db.upsert(app_state.to_json(), AppStateQuery.record_type == APP_STATE_RECORD_TYPE)
        # @important: For now the sequence of following events are important
        # As we first update the cache in the first event which is then used in the second event handler
        self.signals.app_state_updated.emit()
        self.signals.selected_env_changed.emit(environment_name)

    def update_selected_exchange(self, exchange: HttpExchange):
        logging.info(f"API: {exchange.api_call_id} - Selected Exchange {exchange}")
        self.signals.selected_exchange_changed.emit(exchange)

    def upsert_assertions(self, test_case: ApiTestCase):
        ApiTestCaseQuery = Query()
        doc_id = self.db.upsert(
            test_case.to_json(),
            (ApiTestCaseQuery.record_type == API_TEST_CASE_RECORD_TYPE) &
            (ApiTestCaseQuery.api_call_id == test_case.api_call_id)
        )
        logging.info(f"API: {test_case.api_call_id} - New Id: {doc_id} - Upserting API Test case {test_case}")
        self.signals.api_test_case_changed.emit(test_case.api_call_id)
