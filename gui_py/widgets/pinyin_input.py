from PySide6.QtWidgets import *
from PySide6.QtGui import *
from gui_py.font.constants import STYLE, BODY_SIZE

pinyin_regex = r'^[A-Za-z]{1,5}[1-5]?$'


class Label(QLabel):
    def __init__(self):
        super().__init__()

        self.setStyleSheet('QLabel {font-size: ' + str(BODY_SIZE) + 'pt;}')


class LineEdit(QLineEdit):
    def __init__(self):
        super().__init__()

        self.setValidator(QRegularExpressionValidator(pinyin_regex))
        self.setFont(QFont(STYLE, BODY_SIZE))


class PinyinInput(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        self.label = Label()
        self.line_edit = LineEdit()

        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
