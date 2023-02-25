from PyQt6.QtCore import QFile, QFileInfo, QTextStream
from httprider.core.theme_mode import is_dark

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
        pyg_theme = "dark" if is_dark() else "light"
        return styles_from_file(":/themes/pyg-{}.css".format(pyg_theme))
