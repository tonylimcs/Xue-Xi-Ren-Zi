from PySide6.QtWidgets import *

from gui.widgets.label import Label
from gui.widgets.line_edit import LineEdit
from gui.font import size

pinyin_regex = r'^[A-Za-z]{1,5}[1-5]?$'


class PinyinInput(QFrame):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        self.hint = Label()
        self.hint.font_size = size.INPUT_TEXT

        self.line_edit = LineEdit()
        self.line_edit.font_size = size.INPUT_TEXT
        self.line_edit.validator = "pinyin"

        layout.addWidget(self.hint)
        layout.addWidget(self.line_edit)

        layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
