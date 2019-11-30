import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from ..core.constants import REPLACEMENTS
from ..model.app_data import ApiTestCase


def apply_replacements(replacements, input_str):
    return functools.reduce(
        lambda accum, lst: accum.replace(*lst), replacements, input_str
    )


def assertion_variable_name(api_call_title, assertion_source, input_str):
    norm_title = apply_replacements(REPLACEMENTS, api_call_title.lower().strip())
    norm_input = apply_replacements(REPLACEMENTS, input_str.lower())

    if norm_input:
        return f"{ApiTestCase.DEFAULT_VAR_PREFIX}_{norm_title}_{assertion_source}_{norm_input}"
    else:
        return f"{ApiTestCase.DEFAULT_VAR_PREFIX}_{norm_title}_{assertion_source}"


def populate_tree_with_json(json_data, json_model, tree_view):
    json_model.setup_model(json_data)
    tree_view.setModel(json_model)
    tree_view.expandAll()
    tree_view.header().setDefaultAlignment(Qt.AlignHCenter)
    tree_view.header().setSectionResizeMode(0, QHeaderView.Stretch)
    tree_view.header().setSectionResizeMode(1, QHeaderView.Stretch)


def populate_tree_with_kv_dict(kv_dict, tree_widget):
    tree_widget.clear()
    for hn, hv in kv_dict:
        item = QTreeWidgetItem([hn, hv])
        tree_widget.addTopLevelItem(item)


from .assertion_result_presenter import AssertionResultPresenter
from .api_list_presenter import ApiListPresenter
from .config_presenter import ConfigPresenter
from .empty_frame_presenter import EmptyFramePresenter
from .envs_list_presenter import EnvironmentsListPresenter
from .exchange_presenter import ExchangePresenter
from .kv_list_presenter import KeyValueListPresenter
from .main_presenter import MainPresenter
from .importer_presenter import ImporterPresenter
from .assertion_list_presenter import AssertionListPresenter
from .body_assertion_presenter import BodyAssertionPresenter
from .headers_assertions_presenter import HeadersAssertionPresenter
from .assertion_builder_presenter import AssertionBuilderPresenter
from .request_presenter import RequestPresenter
from .tags_list_presenter import TagsListPresenter
from .environment_configuration_presenter import EnvironmentConfigurationPresenter
from .api_calls_history_presenter import ApiCallsHistoryPresenter
from .code_generator_presenter import CodeGeneratorPresenter
from .file_menu_presenter import FileMenuPresenter
from .data_generator_presenter import DataGeneratorPresenter
from .environments_menu_presenter import EnvironmentMenuPresenter
from .fuzz_test_presenter import FuzzTestPresenter
