from PySide6.QtWidgets import *

from gui.widgets.body import Body
from gui.widgets.pinyin_input import PinyinInput


class UpperFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.upper_layout = QVBoxLayout()

        self.body = Body()
        self.pinyin_input = PinyinInput()

        self.upper_layout.addWidget(self.body)
        self.upper_layout.addWidget(self.pinyin_input)

        self.pinyin_input.installEventFilter(self)
