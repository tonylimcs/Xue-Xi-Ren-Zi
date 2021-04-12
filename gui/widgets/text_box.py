from PySide6.QtWidgets import *
from PySide6.QtGui import *


class TextBox(QTextEdit):
    def __init__(self):
        super().__init__()

        self._font_size = 15
        self._read_only = False
        self.sb_width = 12

    @property
    def read_only(self):
        return self._read_only

    @read_only.setter
    def read_only(self, toggle: bool):
        self.setReadOnly(toggle)
        self._read_only = toggle

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, size: int):
        self.__set_style(size=size)
        self._font_size = size

    @property
    def sb_width(self):
        return self._sb_width

    @sb_width.setter
    def sb_width(self, width: int):
        self.__set_style(width=width)
        self._sb_width = width

    def __set_style(self, size: int = '', width: int = ''):
        if not size:
            size = self.font_size

        if not width:
            width = self._sb_width

        self.setStyleSheet('QTextEdit {'
                           'font-size: ' + str(size) + 'pt;'
                           '}'
                           'QScrollBar:vertical {'
                           'width: ' + str(width) + 'px;'
                           '}')
