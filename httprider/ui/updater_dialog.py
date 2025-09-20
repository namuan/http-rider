import json
import sys

from PyQt6 import QtCore
from PyQt6.QtCore import QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt6.QtWidgets import QApplication, QDialog


class Updater(QDialog):
    api_github_latest: QUrl = QUrl("https://api.github.com/repos/namuan/http-rider-osx/releases/latest")
    latest_release_page: QUrl = QUrl("https://github.com/namuan/http-rider-osx/releases/latest")

    def __init__(self, parent=None, flags=QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.WindowCloseButtonHint):
        super().__init__(parent, flags)
        self.parent = parent
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self.done)

    def done(self, reply: QNetworkReply):
        if reply.error() != QNetworkReply.NetworkError.NoError:
            sys.stderr.write(reply.errorString())
            return
        try:
            json_data = json.loads(str(reply.readAll(), "utf-8"))
            reply.deleteLater()
            latest = json_data.get("tag_name")
            current = QApplication.instance().applicationVersion()
            self.parent.update_available(latest, current)
        except json.JSONDecodeError:
            self.logger.exception("Error retrieving data", exc_info=True)
            raise

    def check(self) -> None:
        if self.api_github_latest.isValid():
            self.manager.get(QNetworkRequest(self.api_github_latest))
