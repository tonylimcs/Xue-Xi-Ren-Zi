from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from gui.font.constants import BODY_SIZE


class Label(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        # setting alignment to the text
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # making label multi-line
        self.setWordWrap(True)

        self.setStyleSheet('QLabel {color: gray; '
                           'font-size: ' + str(BODY_SIZE) + 'pt;}')

        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setCursor(QCursor(Qt.IBeamCursor))


class Body(QScrollArea):
    def __init__(self):
        super().__init__()

        # making widget resizable
        self.setWidgetResizable(True)

        # making qwidget object
        content = QWidget(self)
        self.setWidget(content)

        # vertical box layout
        lay = QVBoxLayout(content)

        self.label = Label(content)

        # adding label to the layout
        lay.addWidget(self.label)

        self.setStyleSheet("QScrollArea {"
                           "border: 1px solid gray; "
                           "border-radius: 2px}"
                           "QScrollBar:vertical{width: 12px}")

    def setText(self, text):
        self.label.setText(text)
