from PyQt6.QtGui import QStandardItemModel

from httprider.core import str_to_int
from httprider.core.constants import COMMON_HEADERS, HTTP_CONTENT_TYPES
from httprider.core.core_settings import app_settings
from httprider.core.pygment_styles import pyg_styles
from httprider.exporters.common import highlight_format_json
from httprider.model.app_data import MockedResponse
from httprider.model.completer import get_completer_model
from httprider.presenters.kv_list_presenter import KeyValueListPresenter


class MockedResponsePresenter:
    def __init__(self, parent, parent_view):
        self.parent_presenter = parent
        self.parent_view = parent_view

        self.mocked_response_headers_presenter = KeyValueListPresenter(
            self.parent_view.lst_mocked_response_headers,
            self,
            key_completions=COMMON_HEADERS,
            value_completions=HTTP_CONTENT_TYPES,
        )

        self.parent_view.txt_mocked_response_body.document().setDefaultStyleSheet(pyg_styles())

        app_settings.app_data_reader.signals.initial_cache_loading_completed.connect(self.refresh_completer)
        app_settings.app_data_writer.signals.api_test_case_changed.connect(self.refresh_completer)
        app_settings.app_data_writer.signals.environment_data_changed.connect(self.refresh_completer)

    def refresh_completer(self):
        completer_model: QStandardItemModel = get_completer_model()
        self.parent_view.txt_mocked_response_body.child_edit.setup_completer(completer_model)

    def form_to_object(self):
        mocked_response = MockedResponse()
        mocked_response.is_enabled = self.parent_view.chk_mock_response_enabled.isChecked()
        mocked_response.status_code = str_to_int(self.parent_view.txt_mocked_response_code.text())
        mocked_response.headers = self.mocked_response_headers_presenter.get_items()
        mocked_response.body = self.parent_view.txt_mocked_response_body.toPlainText()
        return mocked_response

    def object_to_form(self, mocked_response: MockedResponse):
        self.parent_view.chk_mock_response_enabled.setChecked(mocked_response.is_enabled)
        self.parent_view.txt_mocked_response_code.setText(str(mocked_response.status_code))
        self.mocked_response_headers_presenter.update_items(mocked_response.headers)
        self.parent_view.txt_mocked_response_body.clear()
        self.parent_view.txt_mocked_response_body.appendHtml(highlight_format_json(mocked_response.body))
