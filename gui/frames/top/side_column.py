from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from gui.widgets.label import Label
from gui.widgets.text_box import TextBox
from gui.font import size


class _Label(Label):
    def __init__(self):
        super().__init__()

        self.alignment = Qt.AlignCenter
        self.font_size = size.SIDE_HEADER


class _TextBox(TextBox):
    def __init__(self):
        super().__init__()

        self.font_size = size.SIDE_MEANING
        self.read_only = True


class SideColumn(QFrame):
    def __init__(self):
        super().__init__()

        self.widget_pairs = self.__create_widget_pairs(2)

        self.grid = QGridLayout()
        self.__add_widget_pairs(self.grid)
        self.grid.setVerticalSpacing(0)

        self.setLayout(self.grid)

        self.is_minimized = False

        self.setMaximumWidth(int(self.width() / 4))

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Resize:
            if self.is_minimized:
                self.setFixedWidth(self.minimumWidth())     # Minimize
                self.is_minimized = True
            else:
                self.setFixedWidth(self.maximumWidth())     # Maximize
                self.is_minimized = False
            return True

        return False

    @staticmethod
    def __create_widget_pairs(num_of_pairs: int) -> list:
        return [(_Label(), _TextBox()) for _ in range(num_of_pairs)]

    def __add_widget_pairs(self, grid_: QGridLayout) -> None:
        row = 0
        for tuples in self.widget_pairs:
            for widget in tuples:
                grid_.addWidget(widget, row, 0)
                row += 1
