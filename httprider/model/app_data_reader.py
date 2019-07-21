import json
import logging
from operator import itemgetter

from PyQt5.QtCore import QObject, pyqtSignal
from tinydb import Query

from httprider.core.constants import API_TEST_CASE_RECORD_TYPE, HTTP_EXCHANGE_RECORD_TYPE, ENVIRONMENT_RECORD_TYPE, \
    PROJECT_INFO_RECORD_TYPE, APP_STATE_RECORD_TYPE, API_CALL_RECORD_TYPE
from httprider.model import ApiCall
from httprider.model.app_data import AppData, ApiTestCase, HttpExchange, Environment, ProjectInfo, AppState


class AppDataReadSignals(QObject):
    api_call_change_selection = pyqtSignal(ApiCall)
    initial_cache_loading_completed = pyqtSignal()


class AppDataReader(AppData):

    def __init__(self, db_table):
        self.db = db_table
        self.signals = AppDataReadSignals()

    def get_api_test_case(self, api_call_id):
        logging.info(f"API: {api_call_id} - Getting API Test case")
        ApiTestCaseQuery = Query()
        return ApiTestCase.from_json(
            self.db.get(
                (ApiTestCaseQuery.record_type == API_TEST_CASE_RECORD_TYPE) &
                (ApiTestCaseQuery.api_call_id == api_call_id)
            ),
            api_call_id
        )

    def get_all_api_calls_from_db(self):
        table = self.ldb[API_CALL_RECORD_TYPE]
        api_calls_db = table.find(name=API_CALL_RECORD_TYPE)
        return {
            api_db['id']: ApiCall.from_json(json.loads(api_db['object']))
            for api_db in api_calls_db
        }

    def get_all_api_calls(self):
        query = Query()
        return {
            obj.doc_id: ApiCall.from_json(obj)
            for obj in sorted(self.db.search(query.type == 'api'), key=itemgetter('sequence_number'))
        }

    def get_api_call(self, doc_id):
        return ApiCall.from_json(self.db.get(doc_id=doc_id))

    def get_api_call_exchanges(self, doc_id):
        query = Query()
        return [
            HttpExchange.from_json(exchange, doc_id)
            for exchange in
            self.db.search((query.type == HTTP_EXCHANGE_RECORD_TYPE) & (query.api_call_id == doc_id))
        ]

    # @todo: Cache and AppState to store the currently selected ApiCall
    # So everyone should look into AppState cache instead of keeping their own copy of current / current_api
    def update_selected_api_call(self, doc_id):
        api_call = ApiCall.from_json(self.db.get(doc_id=doc_id))
        logging.debug(f"update_selected_api_call: {doc_id} = {api_call}")
        self.signals.api_call_change_selection.emit(api_call)

    def get_http_exchange(self, exchange_doc_id):
        return HttpExchange.from_json(self.db.get(doc_id=exchange_doc_id))

    def get_environments(self):
        query = Query()
        return [
            Environment.from_json(obj)
            for obj in self.db.search(query.record_type == ENVIRONMENT_RECORD_TYPE)
        ]

    def get_selected_environment(self, environment_name):
        query = Query()
        return Environment.from_json(
            self.db.get(
                (query.record_type == ENVIRONMENT_RECORD_TYPE) &
                (query.name == environment_name)
            )
        )

    def get_or_create_project_info(self):
        table = self.ldb[PROJECT_INFO_RECORD_TYPE]
        project_info_db = table.find_one(name=PROJECT_INFO_RECORD_TYPE)
        if not project_info_db:
            return ProjectInfo.from_json(None)

        project_info_json = json.loads(project_info_db['object'])
        return ProjectInfo.from_json(project_info_json)

    def get_appstate_environment(self):
        AppStateQuery = Query()
        app_state_json = self.db.get(AppStateQuery.record_type == APP_STATE_RECORD_TYPE)
        app_state = AppState.from_json(app_state_json)
        return app_state.selected_env

    def get_app_state(self):
        AppStateQuery = Query()
        app_state_json = self.db.get(AppStateQuery.record_type == APP_STATE_RECORD_TYPE)
        return AppState.from_json(app_state_json)

    def get_all_env_variables(self):
        current_env = self.get_appstate_environment()
        environment: Environment = self.get_selected_environment(current_env)
        return [
            f"${{{k}}}" for k in environment.data.keys()
        ]

    def get_last_exchange(self, api_call_id):
        api_call_exchanges = self.get_api_call_exchanges(api_call_id)
        if api_call_exchanges:
            return api_call_exchanges[-1]
        else:
            return HttpExchange(api_call_id)
