from PySide6.QtWidgets import *
from PySide6.QtCore import *

from gui.frames.top.body import Body
from gui.frames.top.side_column import SideColumn


class TopFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.body = Body()
        self.side_col = SideColumn()

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.body)
        self.splitter.addWidget(self.side_col)
        self.splitter.setHandleWidth(10)

        self.top_layout = QVBoxLayout()
        self.top_layout.addWidget(self.splitter)
