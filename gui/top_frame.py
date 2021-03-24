from PySide6.QtWidgets import *
from PySide6.QtCore import *

from gui.widgets.body import Body
from gui.widgets.pinyin_input import PinyinInput

from backend.model.classes import handler
from backend.model.constants.event_types import *


class TopFrame(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        self.layout = QVBoxLayout()

        self.body = Body()
        self.pinyin_input = PinyinInput()

        self.layout.addWidget(self.body)
        self.layout.addWidget(self.pinyin_input)

        self.pinyin_input.installEventFilter(self)

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
