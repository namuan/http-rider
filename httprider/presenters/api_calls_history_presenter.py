from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..core.core_settings import app_settings
from ..model.app_data import HttpExchange, ApiCall


class ApiCallsHistoryPresenter:
    def __init__(self, parent):
        self.parent_view = parent
        self.calls_layout = parent.horizontalLayout_6
        self.current_exchange: HttpExchange = None
        self.button_group = QButtonGroup()
        self.button_group.buttonClicked[QAbstractButton].connect(self.handle_exchange_switch)

        app_settings.app_data_writer.signals.exchange_added.connect(self.refresh_on_new_exchange)
        app_settings.app_data_reader.signals.api_call_change_selection.connect(self.refresh_on_api_call_switch)

    def refresh(self):
        for existing_button in self.button_group.buttons():
            existing_button.hide()
            self.calls_layout.removeWidget(existing_button)

        exchanges = app_settings.app_data_cache.get_api_call_exchanges(self.current_exchange.api_call_id)
        for ex in exchanges[-10:]:
            self.on_exchange_added(ex.id, ex)

    def refresh_on_api_call_switch(self, api_call: ApiCall):
        last_exchange = app_settings.app_data_reader.get_last_exchange(api_call.id)
        self.current_exchange = last_exchange
        self.refresh()

    def refresh_on_new_exchange(self, _, exchange: HttpExchange):
        self.current_exchange = exchange
        self.refresh()

    def handle_exchange_switch(self, button):
        selected_exchange_id = button.objectName()
        exchange = app_settings.app_data_cache.get_http_exchange(selected_exchange_id)
        self.current_exchange = exchange
        self.refresh()
        app_settings.app_data_writer.update_selected_exchange(exchange)

    def on_exchange_added(self, exchange_id, exchange: HttpExchange):
        btn = QPushButton(self.parent_view.frame_exchange)
        btn.setMaximumSize(QSize(20, 20))
        if exchange_id == self.current_exchange.id:
            btn.setAccessibleName(self.color_from_response(exchange.response.http_status_code, is_selected=True))
        else:
            btn.setAccessibleName(self.color_from_response(exchange.response.http_status_code))

        btn.setObjectName(f"{exchange_id}")
        self.calls_layout.addWidget(btn)
        self.button_group.addButton(btn)

    def color_from_response(self, response_code, is_selected=False):
        color_code = ""
        if response_code <= 0:
            color_code = "redbox"

        if 100 <= response_code < 400:
            color_code = "greenbox"

        if 400 <= response_code < 500:
            color_code = "amberbox"

        if 500 <= response_code < 600:
            color_code = "redbox"

        if is_selected:
            return "selected" + color_code
        else:
            return color_code
