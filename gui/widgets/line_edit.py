from PySide6.QtWidgets import *
from PySide6.QtGui import *

_pinyin_regex = r'^[A-Za-z]{1,5}[1-5]?$'


class LineEdit(QLineEdit):
    def __init__(self):
        super().__init__()

        self._font_size = 20
        self._validator = None

    @property
    def validator(self):
        return self._validator

    @validator.setter
    def validator(self, type_):
        if type_ == "pinyin":
            validator = QRegularExpressionValidator(_pinyin_regex)
        else:
            validator = QValidator(self)

        self.setValidator(validator)
        self._validator = type_

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, size: int):
        self.setStyleSheet('QLineEdit {font-size: ' + str(size) + 'pt;}')
        self._font_size = size
