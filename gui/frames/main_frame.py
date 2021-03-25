from PySide6.QtWidgets import *
from PySide6.QtCore import *

from gui.widgets.body import Body
from gui.widgets.pinyin_input import PinyinInput
from gui.widgets.side_column import SideColumn

from backend.model.classes import handler
from backend.model.constants.event_types import *

from gui.frames.upper_frame import UpperFrame


class MainFrame(UpperFrame):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.layout.addLayout(self.upper_layout)

        # Set This Layout
        self.setLayout(self.layout)
        self.installEventFilter(self)

        handler.handle(self, event=GUI_INIT)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Return:
                handler.handle(self, event=USER_INPUT)
                self.pinyin_input.line_edit.setText("")     # Reset
                return True

            if key == Qt.Key_Escape:
                self.setText("")
                return True

        return False
