from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from gui.font.constants import STYLE, BODY_SIZE


class Label(QLabel):
    def __init__(self, parent, text):
        super().__init__(parent)

        # setting alignment to the text
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # making label multi-line
        self.setWordWrap(True)

        # setting text font
        self.setFont(QFont(STYLE, BODY_SIZE))

        self.setText(text)


class Body(QScrollArea):
    def __init__(self, text):
        super().__init__()

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        self.label = Label(content, text)

        # adding label to the layout
        lay.addWidget(self.label)

        self.setStyleSheet("QScrollArea {"
                           "border: 1px solid gray; "
                           "border-radius: 2px}"
                           "QScrollBar:vertical{width: 12px}")

    def setText(self, text):
        self.label.setText(text)
