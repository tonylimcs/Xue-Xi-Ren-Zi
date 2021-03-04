from PySide6.QtWidgets import *
from PySide6.QtCore import *

from gui_py.widgets.body import Body
from gui_py.widgets.pinyin_input import PinyinInput

from model.update_gui import update_learning, init_body, init_hint


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

        # Initialize body text and hint
        init_body(self.body)
        init_hint(self.pinyin_input.label)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Return:
                user_input = self.pinyin_input.line_edit.text()
                print(f'input: {user_input} ')
                update_learning(user_input, self.pinyin_input.label, self.body.label)
                self.pinyin_input.line_edit.setText("")
                return True

            if key == Qt.Key_Escape:
                self.setText("")
                return True

        return False
