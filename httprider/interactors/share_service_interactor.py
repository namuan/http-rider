import json
import logging

from PyQt5.QtCore import QUrl, QByteArray, QBuffer
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from httprider.core import str_to_base64_encoded_bytes, bytes_to_str, str_to_bytes
from httprider.core.core_settings import app_settings


class ShareServiceInteractor:
    def __init__(self, view):
        self.view = view
        self.buffer = QBuffer()

        self.network_manager = QNetworkAccessManager(self.view)
        self.network_manager.finished.connect(self.on_received_response)

    def on_received_response(self, reply: QNetworkReply):
        if reply.error() != QNetworkReply.NoError:
            error_msg = "Unable to create new print share: {}".format(
                reply.errorString()
            )
            logging.error(error_msg)
            app_settings.app_data_writer.signals.exchange_share_failed.emit(error_msg)
            return

        share_location = reply.rawHeader(
            QByteArray(bytes("Location", encoding="utf-8"))
        )
        app_settings.app_data_writer.signals.exchange_share_created.emit(
            share_location.data().decode()
        )
        reply.deleteLater()
        self.buffer.close()

    def create_document(self, raw_html):
        app_config = app_settings.load_configuration()
        url: QUrl = QUrl(app_config.print_server + "/prints")
        base64_encoded = str_to_base64_encoded_bytes(raw_html)
        jdoc = {"document": bytes_to_str(base64_encoded)}
        jdoc_str = json.dumps(jdoc)
        self.buffer.setData(str_to_bytes(jdoc_str))
        network_request = QNetworkRequest(url)
        network_request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        in_progress_reply = self.network_manager.post(network_request, self.buffer)
        self.view.finished.connect(in_progress_reply.abort)
