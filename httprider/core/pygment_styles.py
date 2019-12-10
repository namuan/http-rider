from PyQt5.QtCore import QFile, QFileInfo, QTextStream

__pyg_styles = None


def styles_from_file(filename):
    if QFileInfo(filename).exists():
        qss_file = QFile(filename)
        qss_file.open(QFile.ReadOnly | QFile.Text)
        content = QTextStream(qss_file).readAll()
        return content
    else:
        return None


def pyg_styles():
    if __pyg_styles:
        return __pyg_styles
    else:
        return styles_from_file(":/themes/pyg.css")
