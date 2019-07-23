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

    def get_all_api_calls_from_db(self):
        table = self.ldb[API_CALL_RECORD_TYPE]
        api_calls_db = table.find(name=API_CALL_RECORD_TYPE)
        return {
            api_db['api_call_id']: ApiCall.from_json(json.loads(api_db['object']))
            for api_db in api_calls_db
        }

    def get_all_api_calls(self):
        raise SyntaxError("Shouldn't call this method")
        query = Query()
        return {
            obj.doc_id: ApiCall.from_json(obj)
            for obj in sorted(self.db.search(query.type == 'api'), key=itemgetter('sequence_number'))
        }

    def get_api_call_from_db(self, api_call_id):
        logging.info(f"DB: {api_call_id} - Getting API call")
        table = self.ldb[API_CALL_RECORD_TYPE]
        obj_db = table.find_one(name=API_CALL_RECORD_TYPE, api_call_id=api_call_id)
        if not obj_db:
            return ApiCall.from_json()

        return ApiCall.from_json(json.loads(obj_db['object']))

    def get_api_call(self, doc_id):
        raise SyntaxError("Shouldn't call this method")
        # return ApiCall.from_json(self.db.get(doc_id=doc_id))

    def get_api_test_case(self, api_call_id):
        raise SyntaxError("Shouldn't call this method")
        logging.info(f"API: {api_call_id} - Getting API Test case")
        ApiTestCaseQuery = Query()
        return ApiTestCase.from_json(
            self.db.get(
                (ApiTestCaseQuery.record_type == API_TEST_CASE_RECORD_TYPE) &
                (ApiTestCaseQuery.api_call_id == api_call_id)
            ),
            api_call_id
        )

    def get_api_test_case_from_db(self, api_call_id):
        table = self.ldb[API_TEST_CASE_RECORD_TYPE]
        obj_db = table.find_one(name=API_TEST_CASE_RECORD_TYPE, api_call_id=api_call_id)
        if not obj_db:
            return ApiTestCase.from_json(None, api_call_id)

        return ApiTestCase.from_json(
            json.loads(obj_db['object']),
            api_call_id
        )

    def get_api_call_exchanges_from_db(self, doc_id):
        table = self.ldb[HTTP_EXCHANGE_RECORD_TYPE]
        http_exchanges_db = table.find(name=HTTP_EXCHANGE_RECORD_TYPE, api_call_id=doc_id)
        return [
            HttpExchange.from_json(json.loads(obj['object']))
            for obj in http_exchanges_db
            if obj['api_call_id'] == doc_id
        ]

    def get_api_call_exchanges(self, doc_id):
        return self.get_api_call_exchanges_from_db(doc_id)

    # @todo: Cache and AppState to store the currently selected ApiCall
    # So everyone should look into AppState cache instead of keeping their own copy of current / current_api
    def update_selected_api_call(self, doc_id):
        raise SyntaxError("Shouldn't call this method")
        # api_call = ApiCall.from_json(self.db.get(doc_id=doc_id))
        # logging.debug(f"update_selected_api_call: {doc_id} = {api_call}")
        # self.signals.api_call_change_selection.emit(api_call)

    def get_http_exchange_from_db(self, exchange_id):
        table = self.ldb[HTTP_EXCHANGE_RECORD_TYPE]
        http_exchange_db = table.find_one(exchange_id=exchange_id)
        if not http_exchange_db:
            raise LookupError(f"Unable to find exchange with id: {exchange_id}")

        http_exchange_json = json.loads(http_exchange_db['object'])
        return HttpExchange.from_json(http_exchange_json)

    def get_environments_from_db(self):
        table = self.ldb[ENVIRONMENT_RECORD_TYPE]
        environments_db = table.find(name=ENVIRONMENT_RECORD_TYPE)
        if not environments_db:
            return []

        return [
            Environment.from_json(json.loads(obj['object']))
            for obj in environments_db
        ]

    def get_selected_environment_from_db(self, environment_name):
        table = self.ldb[ENVIRONMENT_RECORD_TYPE]
        environment_db = table.find_one(environment_name=environment_name)
        if not environment_db:
            return None

        environment_json = json.loads(environment_db['object'])
        return Environment.from_json(environment_json)

    def get_or_create_project_info(self):
        table = self.ldb[PROJECT_INFO_RECORD_TYPE]
        project_info_db = table.find_one(name=PROJECT_INFO_RECORD_TYPE)
        if not project_info_db:
            return ProjectInfo.from_json(None)

        project_info_json = json.loads(project_info_db['object'])
        return ProjectInfo.from_json(project_info_json)

    def get_appstate_environment(self):
        app_state = self.get_app_state()
        return app_state.selected_env

    def get_app_state(self):
        table = self.ldb[APP_STATE_RECORD_TYPE]
        app_state_db = table.find_one(name=APP_STATE_RECORD_TYPE)
        if not app_state_db:
            return AppState.from_json()

        app_state_json = json.loads(app_state_db['object'])
        return AppState.from_json(app_state_json)
