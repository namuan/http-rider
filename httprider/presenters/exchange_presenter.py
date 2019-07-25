import logging

from PyQt5.QtWidgets import QHeaderView

from ..core import elapsed_time_formatter, response_code_formatter, styles_from_file
from ..core.core_settings import app_settings
from ..exporters import request_body_highlighted, response_body_highlighted
from ..model.app_data import ApiCall, HttpExchange
from . import populate_tree_with_kv_dict


class ExchangePresenter:
    def __init__(self, parent_view):
        self.current: ApiCall = None
        self.view = parent_view
        self.pyg_styles = styles_from_file(":/themes/pyg.css")
        self.view.txt_exchange_request_body.document().setDefaultStyleSheet(self.pyg_styles)
        self.view.txt_response_body.document().setDefaultStyleSheet(self.pyg_styles)

        self.view.tbl_exchange_request_headers.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.view.tbl_exchange_request_headers.header().setSectionResizeMode(1, QHeaderView.Stretch)
        self.view.tbl_exchange_request_params.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.view.tbl_exchange_request_params.header().setSectionResizeMode(1, QHeaderView.Stretch)
        self.view.tbl_exchange_form_params.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.view.tbl_exchange_form_params.header().setSectionResizeMode(1, QHeaderView.Stretch)
        self.view.tbl_response_headers.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.view.tbl_response_headers.header().setSectionResizeMode(1, QHeaderView.Stretch)

        app_settings.app_data_writer.signals.exchange_added.connect(self.refresh)
        app_settings.app_data_reader.signals.api_call_change_selection.connect(self.display_last_exchange)
        app_settings.app_data_writer.signals.selected_exchange_changed.connect(self.on_exchange_changed)

    def display_last_exchange(self, api_call: ApiCall):
        api_call_exchanges = app_settings.app_data_cache.get_api_call_exchanges(api_call.id)
        if api_call_exchanges:
            last_exchange = api_call_exchanges[-1]
            self.refresh(api_call.id, last_exchange)
        else:
            self.refresh(api_call.id, HttpExchange(api_call.id))

    def on_exchange_changed(self, exchange: HttpExchange):
        self.refresh(exchange.api_call_id, exchange)

    def cleanup(self):
        """Called when all API calls are removed from list"""
        self.view.frame_exchange.hide()

    def refresh(self, api_call_id, exchange: HttpExchange):
        api_call = app_settings.app_data_cache.get_api_call(api_call_id)
        logging.info(f"API Call {api_call_id} - Updating Exchange View: {api_call}")
        self.current = api_call
        http_request = exchange.request
        # Request rendering
        self.view.lbl_request_title.setText(f"{http_request.http_method} {http_request.http_url}")
        self.view.lbl_request_time.setText(http_request.request_time)

        self.view.txt_exchange_request_body.setHtml(request_body_highlighted(http_request))
        populate_tree_with_kv_dict(
            http_request.headers.items(),
            self.view.tbl_exchange_request_headers
        )
        populate_tree_with_kv_dict(
            http_request.query_params.items(),
            self.view.tbl_exchange_request_params
        )
        populate_tree_with_kv_dict(
            http_request.form_params.items(),
            self.view.tbl_exchange_form_params
        )

        http_response = exchange.response

        # Response rendering
        response_code = response_code_formatter(http_response.http_status_code)
        self.view.lbl_response_code.setText(f"HTTP {response_code}")
        elapsed_time = elapsed_time_formatter(http_response.elapsed_time)
        self.view.lbl_response_latency.setText(elapsed_time)
        self.view.txt_response_body.setHtml(response_body_highlighted(http_response))

        populate_tree_with_kv_dict(
            http_response.headers.items(),
            self.view.tbl_response_headers
        )
