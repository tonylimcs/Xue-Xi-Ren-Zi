from PySide6.QtWidgets import *

from backend.model.classes.body import Body
from backend.model.classes.current import Current


def __update_body_label(body_label: QLabel, body: Body) -> None:
    body_label.setText(body.body_html)


def __update_hint_label(hint_label: QLabel, cur: Current) -> None:
    hanzi = cur.char.hanzi if cur.char is not None else ''
    hint_label.setText(hanzi)


def update_text(*args: tuple):
    for arg in args:
        if isinstance(arg[0], QWidget):
            if isinstance(arg[1], Body):
                __update_body_label(arg[0], arg[1])
            elif isinstance(arg[1], Current):
                __update_hint_label(arg[0], arg[1])
