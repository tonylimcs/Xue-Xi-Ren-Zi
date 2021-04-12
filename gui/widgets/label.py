from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


class Label(QLabel):
    def __init__(self, parent=''):
        super().__init__(parent)

        self._font_size = 20
        self._font_color = 'black'
        self._alignment = (Qt.AlignLeft | Qt.AlignVCenter)
        self._interactive = False

        self.setWordWrap(True)

    @property
    def alignment(self) -> Qt.Alignment:
        return self._alignment

    @alignment.setter
    def alignment(self, alignment_: Qt.Alignment) -> None:
        self.setAlignment(alignment_)
        self._alignment = alignment_

    @property
    def font_size(self) -> int:
        return self._font_size

    @font_size.setter
    def font_size(self, size: int) -> None:
        self.__set_style(size=size)
        self._font_size = size

    @property
    def font_color(self) -> str:
        return self._font_color

    @font_color.setter
    def font_color(self, color: str) -> None:
        self.__set_style(color=color)
        self._font_color = color

    @property
    def interactive(self) -> bool:
        return self._interactive

    @interactive.setter
    def interactive(self, is_interactive: bool) -> None:
        if is_interactive:
            self.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.setCursor(QCursor(Qt.IBeamCursor))
        else:
            self.setTextInteractionFlags(Qt.NoTextInteraction)
            self.setCursor(QCursor(Qt.ArrowCursor))

        self._interactive = is_interactive

    def __set_style(self, color: str = '', size: int = ''):
        if not color:
            color = self.font_color

        if not size:
            size = self.font_size

        self.setStyleSheet('QLabel {'
                           'color: ' + color + '; '
                           'font-size: ' + str(size) + 'pt;'
                           '}')
