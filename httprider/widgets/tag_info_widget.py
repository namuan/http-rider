from PyQt5.QtWidgets import QWidget

from ..generated.tag_info_widget import Ui_TagInfoWidget
from ..model.app_data import TagInfo


class TagInfoWidget(QWidget, Ui_TagInfoWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setLayout(self.horizontalLayout)

    def setData(self, tag_info: TagInfo):
        self.lbl_tag.setText(tag_info.name)
        self.txt_tag_info.setPlainText(tag_info.description)

    def getData(self):
        return TagInfo(
            name=self.lbl_tag.text(), description=self.txt_tag_info.toPlainText()
        )
