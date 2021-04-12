from PySide6.QtWidgets import *
from PySide6.QtCore import *

from backend.model.classes import handler
from backend.model.constants.event_types import *

from gui.frames.top_frame import TopFrame
from gui.frames.bottom_frame import BottomFrame


class MainFrame(TopFrame, BottomFrame):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.layout.addLayout(self.top_layout)
        self.layout.addLayout(self.bottom_layout)

        # Set This Layout
        self.setLayout(self.layout)

        handler.handle(self, event=GUI_INIT)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Return:
                handler.handle(self, event=USER_INPUT)
                self.clear_input()
                return True

            if key == Qt.Key_Escape:
                self.clear_input()
                return True

        return False

    def clear_input(self):
        self.pinyin_input.line_edit.clear()
