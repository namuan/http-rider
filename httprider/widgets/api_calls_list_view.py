from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ..core.constants import API_CALL_ROLE
from ..model.app_data import ApiCall

PADDING = 5


class ApiCallItemDelegate(QStyledItemDelegate):
    TITLE_FONT_SIZE = 12
    TITLE_FONT_BOLD = True
    URL_FONT_SIZE = 10
    URL_FONT_BOLD = False
    GREEN_COLOR = QColor("#01721d")
    AMBER_COLOR = QColor("#d8a413")
    RED_COLOR = QColor("#a51e00")

    def sizeHint(self, option: QStyleOptionViewItem, model_index: QModelIndex):
        if not model_index.isValid():
            return

        bounding_rect = option.rect

        api_call: ApiCall = model_index.data(API_CALL_ROLE)

        if api_call.is_separator:
            size: QSize = QSize(option.rect.width(), 5)
            return size

        api_title = api_call.title
        api_http_url = f"{api_call.http_method} {api_call.http_url}"

        # title
        font: QFont = QApplication.font()
        font.setPointSize(self.TITLE_FONT_SIZE)
        font.setBold(self.TITLE_FONT_BOLD)
        font_metrics: QFontMetrics = QFontMetrics(font)
        title_rect = font_metrics.boundingRect(
            0, 0, bounding_rect.width(), 0, Qt.AlignLeft | Qt.AlignTop, api_title
        )

        # http url + method
        font.setPointSize(self.URL_FONT_SIZE)
        font.setBold(self.URL_FONT_BOLD)
        font_metrics: QFontMetrics = QFontMetrics(font)
        url_rect = font_metrics.boundingRect(
            0, 0, bounding_rect.width(), 0, Qt.AlignLeft | Qt.AlignTop, api_http_url
        )
        size: QSize = QSize(
            option.rect.width(), title_rect.height() + url_rect.height() + 10 * PADDING
        )

        return size

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, model_index: QModelIndex
    ):
        if not model_index.isValid():
            return

        bounding_rect = option.rect
        painter.save()

        if option.state & QStyle.State_Selected:
            painter.fillRect(bounding_rect, QColor("#CBD8E1"))
            painter.setPen(QColor("#000000"))

        api_call: ApiCall = model_index.data(API_CALL_ROLE)

        if api_call.is_separator:
            painter.fillRect(bounding_rect, QColor("#404040"))
            painter.restore()
            return

        api_title = api_call.title
        api_http_url = f"{api_call.http_method} {api_call.http_url}"
        api_status_code = (
            str(api_call.last_response_code) if api_call.last_response_code else None
        )

        title_pen_color = Qt.black
        sub_title_pen_color = Qt.black

        if not api_call.enabled:
            painter.fillRect(bounding_rect, QColor("#cfd2d6"))
            title_pen_color = Qt.gray
            sub_title_pen_color = Qt.gray

        font: QFont = QApplication.font()
        font.setPointSize(self.TITLE_FONT_SIZE)
        font.setBold(self.TITLE_FONT_BOLD)
        font_metrics: QFontMetrics = QFontMetrics(font)
        elided_title = font_metrics.elidedText(
            api_title, Qt.ElideRight, bounding_rect.width() - 10 * PADDING
        )
        # title
        title_rect = font_metrics.boundingRect(
            bounding_rect.left() + PADDING,
            bounding_rect.top() + PADDING,
            bounding_rect.width() - 10 * PADDING,
            0,
            Qt.AlignLeft | Qt.AlignTop,
            elided_title,
        )
        painter.setFont(font)
        painter.setPen(title_pen_color)
        painter.drawText(
            title_rect, Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap, elided_title
        )

        self.draw_status_code(
            title_rect, bounding_rect, painter, api_status_code, api_call
        )

        # http url
        font.setPointSize(self.URL_FONT_SIZE)
        font.setBold(self.URL_FONT_BOLD)
        font_metrics: QFontMetrics = QFontMetrics(font)
        elided_http_url = font_metrics.elidedText(
            api_http_url, Qt.ElideMiddle, bounding_rect.width() - 5 * PADDING
        )

        url_rect = font_metrics.boundingRect(
            title_rect.left(),
            title_rect.bottom() + 2 * PADDING,
            bounding_rect.width() - PADDING,
            0,
            Qt.AlignLeft | Qt.AlignTop,
            elided_http_url,
        )
        painter.setFont(font)
        painter.setPen(sub_title_pen_color)
        painter.drawText(
            url_rect, Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap, elided_http_url
        )

        painter.restore()

    def draw_status_code(
        self, title_rect, bounding_rect, painter, api_status_code, api_call
    ):
        code_rect_width = api_status_code * 2 if api_status_code else ""

        font: QFont = QApplication.font()
        font.setPointSize(10)
        font_metrics: QFontMetrics = QFontMetrics(font)
        code_rect: QRect = font_metrics.boundingRect(
            title_rect.right() + 2 * PADDING,
            title_rect.top(),
            bounding_rect.width() - 10 * PADDING,
            0,
            Qt.AlignLeft | Qt.AlignTop,
            code_rect_width,
        )
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(code_rect), 5, 5)

        if api_status_code:
            color = self.color_from_response(api_call.last_response_code)
            color_assertions = self.color_from_assertions(
                api_call.last_assertion_result, color
            )
            gradient: QLinearGradient = QLinearGradient(
                code_rect.topLeft(), code_rect.bottomRight()
            )
            gradient.setColorAt(0, color)
            gradient.setColorAt(1, color_assertions)
            painter.fillPath(path, gradient)
            painter.setFont(font)
            painter.setPen(Qt.white)
            if api_call.last_response_code > 0:
                painter.drawText(
                    code_rect, Qt.AlignCenter | Qt.AlignVCenter, api_status_code
                )

    def color_from_assertions(self, assertion_result, response_color):
        if assertion_result is None:
            return response_color

        if assertion_result is False:
            return self.RED_COLOR

        return self.GREEN_COLOR

    def color_from_response(self, response_code):
        if response_code <= 0:
            return QColor("#a51e00")

        if 100 <= response_code < 400:
            return self.GREEN_COLOR

        if 400 <= response_code < 500:
            return self.AMBER_COLOR

        if 500 <= response_code < 600:
            return self.RED_COLOR


class ApiCallsListView(QListView):
    drop_event_signal = pyqtSignal(QModelIndex)

    def __init__(self, parent=None):
        super(QListView, self).__init__(parent)

    def dropEvent(self, e: QDropEvent):
        super(QListView, self).dropEvent(e)
        model_index = self.indexAt(e.pos())
        self.drop_event_signal.emit(model_index)
