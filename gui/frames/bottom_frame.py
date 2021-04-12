from PySide6.QtWidgets import *

from gui.frames.bottom.pinyin_input import PinyinInput


class BottomFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.pinyin_input = PinyinInput()
        self.pinyin_input.installEventFilter(self)

        self.bottom_layout = QVBoxLayout()
        self.bottom_layout.addWidget(self.pinyin_input)
