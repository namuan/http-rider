import logging

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from httprider.core.core_settings import app_settings
from httprider.model.app_data import ApiCall, HttpExchange


class ApiCallsHistoryPresenter:
    def __init__(self, parent):
        self.parent_view = parent
        self.calls_layout = parent.horizontalLayout_6
        self.current_exchange: HttpExchange = None
        self.button_group = QButtonGroup()
        self.button_group.buttonClicked[QAbstractButton].connect(self.handle_exchange_switch)

        app_settings.app_data_writer.signals.exchange_added.connect(self.refresh_on_new_exchange)
        app_settings.app_data_reader.signals.api_call_change_selection.connect(self.refresh_on_api_call_switch)
        logging.debug("ApiCallsHistoryPresenter initialized and signals connected")

    def refresh(self):
        if not self.current_exchange:
            logging.debug("Refresh skipped: current_exchange is None")
            return

        for existing_button in self.button_group.buttons():
            existing_button.hide()
            self.calls_layout.removeWidget(existing_button)
            logging.debug("Removed existing exchange button: %s", existing_button.objectName())

        exchanges = app_settings.app_data_cache.get_api_call_exchanges(self.current_exchange.api_call_id)
        logging.debug(
            "Refreshing exchange buttons for api_call_id=%s; total_exchanges=%d",
            self.current_exchange.api_call_id,
            len(exchanges) if exchanges else 0,
        )
        for ex in exchanges[-10:]:
            self.on_exchange_added(ex.id, ex)

    def refresh_on_api_call_switch(self, api_call: ApiCall):
        last_exchange = app_settings.app_data_cache.get_last_exchange(api_call.id)
        self.current_exchange = last_exchange
        logging.debug(
            "API call switched: api_call_id=%s, last_exchange_id=%s",
            api_call.id,
            last_exchange.id if last_exchange else None,
        )
        self.refresh()

    def refresh_on_new_exchange(self, exchange: HttpExchange):
        self.current_exchange = exchange
        logging.debug("New exchange received: exchange_id=%s", exchange.id)
        self.refresh()

    def handle_exchange_switch(self, button):
        selected_exchange_id = button.objectName()
        exchange = app_settings.app_data_cache.get_http_exchange(selected_exchange_id)
        self.current_exchange = exchange
        logging.debug(
            "Exchange switch: selected_exchange_id=%s, response_code=%s",
            selected_exchange_id,
            exchange.response.http_status_code if exchange and exchange.response else None,
        )
        self.refresh()
        app_settings.app_data_writer.update_selected_exchange(exchange)

    def on_exchange_added(self, exchange_id, exchange: HttpExchange):
        btn = QPushButton(self.parent_view.frame_exchange)
        btn.setMaximumSize(QSize(20, 20))
        is_selected = exchange_id == self.current_exchange.id
        color_name = self.color_from_response(exchange.response.http_status_code, is_selected=is_selected)
        btn.setAccessibleName(color_name)

        btn.setObjectName(f"{exchange_id}")
        self.calls_layout.addWidget(btn)
        self.button_group.addButton(btn)
        logging.debug(
            "Added exchange button: exchange_id=%s, accessibleName=%s, selected=%s",
            exchange_id,
            color_name,
            is_selected,
        )

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

        result = ("selected" + color_code) if is_selected else color_code
        logging.debug(
            "Computed color from response: code=%s, selected=%s -> %s",
            response_code,
            is_selected,
            result,
        )
        return result
