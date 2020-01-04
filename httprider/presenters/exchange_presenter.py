import logging

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QHeaderView
from mistune import markdown

from httprider.core.core_settings import app_settings
from httprider.core.pygment_styles import pyg_styles
from httprider.exporters.common import (
    request_body_highlighted,
    response_body_highlighted,
)
from httprider.model.app_data import ApiCall, HttpExchange
from httprider.presenters import populate_tree_with_kv_dict
from httprider.presenters.common import markdown_request, markdown_response


class ExchangePresenter:
    def __init__(self, parent_view):
        self.current: ApiCall = None
        self.current_exchange: HttpExchange = None
        self.view = parent_view
        self.view.txt_raw_request.document().setDefaultStyleSheet(pyg_styles())
        self.view.txt_raw_response.document().setDefaultStyleSheet(pyg_styles())

        self.view.txt_exchange_request_body.document().setDefaultStyleSheet(pyg_styles())
        self.view.txt_response_body.document().setDefaultStyleSheet(pyg_styles())

        self.view.tbl_exchange_request_headers.header().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.view.tbl_exchange_request_headers.header().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.view.tbl_exchange_request_params.header().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.view.tbl_exchange_request_params.header().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.view.tbl_exchange_form_params.header().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.view.tbl_exchange_form_params.header().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.view.tbl_response_headers.header().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.view.tbl_response_headers.header().setSectionResizeMode(
            1, QHeaderView.Stretch
        )

        # ui events
        self.view.btn_share_preview.clicked.connect(self.open_share_preview)

        # domain events
        app_settings.app_data_writer.signals.exchange_added.connect(self.refresh)
        app_settings.app_data_reader.signals.api_call_change_selection.connect(
            self.display_last_exchange
        )
        app_settings.app_data_writer.signals.selected_exchange_changed.connect(
            self.on_exchange_changed
        )

    def open_share_preview(self):
        self.view.share_preview_dialog.show_exchange_preview(self.current_exchange)

    def display_last_exchange(self, api_call: ApiCall):
        api_call_exchanges = app_settings.app_data_cache.get_api_call_exchanges(
            api_call.id
        )
        if api_call_exchanges:
            last_exchange = api_call_exchanges[-1]
            self.refresh(last_exchange)
        else:
            self.refresh(HttpExchange(api_call.id))

    def on_exchange_changed(self, exchange: HttpExchange):
        self.refresh(exchange)

    def cleanup(self):
        """Called when all API calls are removed from list"""
        self.view.frame_exchange.hide()

    def render_raw_exchange(self, plain_text_widget, raw_content):
        plain_text_widget.clear()
        plain_text_widget.appendHtml(markdown(raw_content))
        txt_cursor: QTextCursor = plain_text_widget.textCursor()
        txt_cursor.movePosition(QTextCursor.Start)
        plain_text_widget.setTextCursor(txt_cursor)

    def refresh(self, exchange: HttpExchange):
        self.current_exchange = exchange
        api_call_id = exchange.api_call_id
        api_call = app_settings.app_data_cache.get_api_call(api_call_id)
        logging.info(f"API Call {api_call_id} - Updating Exchange View: {api_call}")
        self.current = api_call
        http_request = exchange.request
        # Request rendering
        self.view.lbl_request_time.setText(http_request.request_time)
        self.render_raw_exchange(self.view.txt_raw_request, markdown_request(exchange))

        self.view.txt_exchange_request_body.setHtml(
            request_body_highlighted(http_request)
        )
        populate_tree_with_kv_dict(
            http_request.headers.items(), self.view.tbl_exchange_request_headers
        )
        populate_tree_with_kv_dict(
            http_request.query_params.items(), self.view.tbl_exchange_request_params
        )
        populate_tree_with_kv_dict(
            http_request.form_params.items(), self.view.tbl_exchange_form_params
        )

        http_response = exchange.response

        # @todo: How to highlight mocked response
        # Response rendering
        # if http_response.is_mocked:
        #     self.view.txt_raw_response.setStyleSheet("background-color: #e0d7d7;")
        # else:
        #     self.view.txt_raw_response.setStyleSheet("background-color: white;")

        self.render_raw_exchange(
            self.view.txt_raw_response, markdown_response(exchange)
        )

        self.view.txt_response_body.setHtml(response_body_highlighted(http_response))

        populate_tree_with_kv_dict(
            http_response.headers.items(), self.view.tbl_response_headers
        )
