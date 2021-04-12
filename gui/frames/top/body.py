from PySide6.QtWidgets import *

from gui.widgets.label import Label
from gui.font import size


class _Text(Label):
    def __init__(self, parent):
        super().__init__(parent)

        self.font_size = size.BODY_TEXT
        self.font_color = 'gray'   # default
        self.interactive = True


class Body(QScrollArea):
    def __init__(self):
        super().__init__()

        # making widget resizable
        self.setWidgetResizable(True)

        # making QWidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        self.text = _Text(content)

        # adding label to the layout
        lay.addWidget(self.text)

        self.setStyleSheet("QScrollArea {"
                           "border: 1px solid gray; "
                           "border-radius: 2px}"
                           "QScrollBar:vertical{width: 12px}")
