from PySide6.QtWidgets import QWidget

from model.text_formatter import update_format
from model.data import data

from engine.checker import check_correct


def update_text_gui(*args):
    for arg in args:
        if isinstance(arg[0], QWidget) and type(arg[1]) is str:
            arg[0].setText(arg[1])


def init_body(widget: QWidget):
    update_text_gui((widget, data.text))


def init_hint(widget: QWidget):
    cur_pos = data.learning_pos[0][0]
    hint = data.tokens[cur_pos]
    update_text_gui((widget, hint))


def update_learning(user_input: str, hint_widget: QWidget, body_widget: QWidget):
    is_correct, cur_char, cur_pinyin = check_correct(user_input, data.learning_pos, data.tokens)
    next_pos = data.learning_pos[0][0]
    next_char = data.tokens[next_pos]
    data.text = update_format(data.text, cur_char, cur_pinyin, next_char, correct=is_correct)
    update_text_gui((hint_widget, next_char),
                    (body_widget, data.text))
