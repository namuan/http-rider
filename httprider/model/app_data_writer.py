import json
import logging

from PyQt6.QtCore import QObject, pyqtSignal

from ..core import gen_uuid
from ..core.constants import ENVIRONMENT_RECORD_TYPE, API_CALL_RECORD_TYPE
from ..model.app_data import (
    HttpExchange,
    ApiCall,
    ProjectInfo,
    AppData,
    Environment,
    ApiTestCase,
)


class AppDataSignals(QObject):
    exchange_added = pyqtSignal(HttpExchange)
    exchange_changed = pyqtSignal(str, HttpExchange)
    api_call_added = pyqtSignal(str, ApiCall)
    api_call_removed = pyqtSignal(list)
    api_call_updated = pyqtSignal(str, ApiCall)
    multiple_api_calls_added = pyqtSignal(list, list)
    selected_tag_changed = pyqtSignal(str)
    selected_env_changed = pyqtSignal(str)
    api_call_tag_added = pyqtSignal(ApiCall, str)
    api_call_tag_removed = pyqtSignal(ApiCall, str)
    environment_added = pyqtSignal(str)
    environment_removed = pyqtSignal()
    environment_renamed = pyqtSignal()
    environment_data_changed = pyqtSignal(str)
    api_test_case_changed = pyqtSignal(str)
    selected_exchange_changed = pyqtSignal(HttpExchange)
    project_info_updated = pyqtSignal(ProjectInfo)
    app_state_updated = pyqtSignal()
    environments_imported = pyqtSignal()
    exchange_share_created = pyqtSignal(str)
    exchange_share_failed = pyqtSignal(str)


class AppDataWriter(AppData):
    def __init__(self, db_table):
        self.ldb = db_table
        self.signals = AppDataSignals()

    def update_project_info(self, project_info):
        if not project_info:
            return

        logging.info(f"Updating Project info In DB {project_info}")
        table = self.ldb[project_info.record_type]
        table.upsert(
            dict(
                name=project_info.record_type, object=json.dumps(project_info.to_json())
            ),
            ["name"],
        )
        self.signals.project_info_updated.emit(project_info)

    def update_app_state(self, app_state):
        if not app_state:
            return

        logging.info(f"Updating App State In DB {app_state}")
        table = self.ldb[app_state.record_type]
        table.upsert(
            dict(name=app_state.record_type, object=json.dumps(app_state.to_json())),
            ["name"],
        )
        self.signals.app_state_updated.emit()

    def update_http_exchange_in_db(self, exchange: HttpExchange):
        table = self.ldb[exchange.type]
        table.upsert(
            dict(
                name=exchange.type,
                exchange_id=exchange.id,
                api_call_id=exchange.api_call_id,
                object=json.dumps(exchange.to_json()),
            ),
            ["exchange_id", "api_call_id"],
        )

    def add_http_exchange(self, exchange: HttpExchange):
        exchange.id = gen_uuid()
        self.update_http_exchange_in_db(exchange)
        logging.info(f"API {exchange.api_call_id} - Added http exchange {exchange.id}")
        self.signals.exchange_added.emit(exchange)

    def update_http_exchange(self, exchange: HttpExchange):
        logging.info(
            f"API {exchange.api_call_id} - Updating http exchange {exchange.id}"
        )
        self.update_http_exchange_in_db(exchange)
        self.signals.exchange_changed.emit(exchange.id, exchange)

    def update_selected_exchange(self, exchange: HttpExchange):
        logging.info(f"API: {exchange.api_call_id} - Selected Exchange {exchange}")
        self.signals.selected_exchange_changed.emit(exchange)

    def update_api_call_in_db(self, api_call: ApiCall):
        logging.debug(f"update_api_call_in_db - {api_call}")
        table = self.ldb[api_call.type]
        table.upsert(
            dict(
                name=api_call.type,
                api_call_id=api_call.id,
                object=json.dumps(api_call.to_json()),
            ),
            ["api_call_id"],
        )
        return api_call.id

    def delete_api_call_from_db(self, api_call_ids):
        table = self.ldb[API_CALL_RECORD_TYPE]
        for api_call_id in api_call_ids:
            table.delete(api_call_id=api_call_id)

    def update_environment_in_db(self, environment: Environment):
        table = self.ldb[environment.record_type]
        table.upsert(
            dict(
                name=environment.record_type,
                environment_name=environment.name,
                object=json.dumps(environment.to_json()),
            ),
            ["environment_name"],
        )

    def update_environment_name_in_db(self, old_environment_name, new_environment_name):
        self.remove_environment_from_db(old_environment_name)
        self.update_environment_in_db(new_environment_name)

    def remove_environment_from_db(self, environment_name):
        table = self.ldb[ENVIRONMENT_RECORD_TYPE]
        table.delete(environment_name=environment_name)
        logging.info(f"Removed environment {environment_name}")

    def upsert_assertions(self, test_case: ApiTestCase):
        if not test_case.id:
            test_case.id = gen_uuid()

        table = self.ldb[test_case.record_type]
        table.upsert(
            dict(
                name=test_case.record_type,
                test_case_id=test_case.id,
                api_call_id=test_case.api_call_id,
                object=json.dumps(test_case.to_json()),
            ),
            ["test_case_id"],
        )

        logging.info(
            f"API: {test_case.api_call_id} - Test Id: {test_case.id} - Upserting API Test case {test_case}"
        )
        self.signals.api_test_case_changed.emit(test_case.api_call_id)
