from PySide6.QtWidgets import *
from PySide6.QtGui import *
from gui.font.constants import STYLE, BODY_SIZE


class Label(QLabel):
    def __init__(self, text: str):
        super().__init__()
        self.setText(text)


class Body(Label):
    def __init__(self, text: str):
        super().__init__(text)
        self.setFont(QFont(STYLE, BODY_SIZE))
        self.setStyleSheet("QLabel { "
                           "border: 1px solid gray; "
                           "border-radius: 2px; "
                           "background-color: none; "
                           "padding: 0px 0px 0px 5px;}")
