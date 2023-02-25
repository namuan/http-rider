import json
import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt6.QtWidgets import qApp, QDialog


class Updater(QDialog):
    api_github_latest: QUrl = QUrl(
        "https://api.github.com/repos/namuan/http-rider-osx/releases/latest"
    )
    latest_release_page: QUrl = QUrl(
        "https://github.com/namuan/http-rider-osx/releases/latest"
    )

    def __init__(self, parent=None, flags=Qt.Dialog | Qt.WindowCloseButtonHint):
        super(Updater, self).__init__(parent, flags)
        self.parent = parent
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self.done)

    def done(self, reply: QNetworkReply):
        if reply.error() != QNetworkReply.NoError:
            sys.stderr.write(reply.errorString())
            return
        try:
            json_data = json.loads(str(reply.readAll(), "utf-8"))
            reply.deleteLater()
            latest = json_data.get("tag_name")
            current = qApp.applicationVersion()
            self.parent.update_available(latest, current)
        except json.JSONDecodeError:
            self.logger.exception("Error retrieving data", exc_info=True)
            raise

    def check(self) -> None:
        if self.api_github_latest.isValid():
            self.manager.get(QNetworkRequest(self.api_github_latest))
