from PyQt6.QtGui import QStandardItem, QStandardItemModel

from httprider.core.constants import DYNAMIC_STRING_ROLE
from httprider.model.app_data import ApiTestCase

from ..core.core_settings import app_settings


def get_completer_model():
    model: QStandardItemModel = QStandardItemModel()

    envs = app_settings.app_data_cache.get_all_env_variables()
    for e in envs:
        item: QStandardItem = QStandardItem()
        item.setText(e)
        item.setData(e, DYNAMIC_STRING_ROLE)
        model.appendRow(item)

    api_calls = app_settings.app_data_cache.get_all_api_calls()
    for api in api_calls:
        api_test_case: ApiTestCase = app_settings.app_data_cache.get_api_test_case(api.id)
        for assertion in api_test_case.assertions:
            item: QStandardItem = QStandardItem()
            item.setText(f"${{{api.title} > ${assertion.var_name}}}")
            item.setData(f"${{{assertion.var_name}}}", DYNAMIC_STRING_ROLE)
            model.appendRow(item)

    # Triggers custom dialog boxes
    for func_keyword in ["data", "file", "tools"]:
        item: QStandardItem = QStandardItem()
        item.setText(func_keyword)
        item.setData(func_keyword, DYNAMIC_STRING_ROLE)
        model.appendRow(item)

    return model
