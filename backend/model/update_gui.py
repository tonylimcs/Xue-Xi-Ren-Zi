from PySide6.QtWidgets import QWidget

from backend.model.text_formatter import update_format, update_highlight, update_domino_effect
from backend.model.data import data

from backend.engine.checker import check_correct
from backend.keys import *


def update_text_gui(*args: tuple):
    """
    Set the text of the widget
    :param args: (QWidget, str)
    """
    for arg in args:
        if isinstance(arg[0], QWidget) and type(arg[1]) is str:
            arg[0].setText(arg[1])


def init_body(widget: QWidget):
    update_text_gui((widget, data.text))


def init_hint(widget: QWidget):
    hint = ""
    if len(data.learning_pos) > 0:
        cur_pos = data.learning_pos[0][0]
        hint = data.tokens[cur_pos]
    update_text_gui((widget, hint))


def update_learning(user_input: str, hint_widget: QWidget, body_widget: QWidget):
    if len(data.learning_pos) <= 0:
        return

    is_correct, cur_char, cur_pinyin = check_correct(user_input, data.learning_pos, data.tokens)
    data.update_counter(cur_char, cur_pinyin, is_correct)

    while len(data.learning_pos) > 0:
        tup = data.learning_pos[0]
        next_pos, next_pinyin = tup[0], tup[1]
        next_char = data.tokens[next_pos]
        state = data.find_state(next_char, next_pinyin)
        if state != LEARNING:
            # Update list
            data.learning_pos.pop(0)
        else:
            break
    else:
        data.update_json()  # Only update at the end
        next_char = ""

    data.text = update_format(data.text, cur_char, cur_pinyin, is_correct)

    data.text = update_highlight(data.text, next_char)

    counter = data.get_counter(cur_char, cur_pinyin)
    data.text = update_domino_effect(data.text, cur_char, counter)

    update_text_gui((hint_widget, next_char),
                    (body_widget, data.text))
