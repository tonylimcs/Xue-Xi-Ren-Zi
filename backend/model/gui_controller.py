from gui.frames.top.body import Body as Body_UI
from gui.frames.top.side_column import SideColumn
from gui.frames.bottom.pinyin_input import PinyinInput

from backend.model.classes.body import Body
from backend.model.classes.current import Current


def __update_body_label(frame: Body_UI, body: Body) -> None:
    frame.text.setText(body.body_html)


def __update_side_col(frame: SideColumn, cur: Current) -> None:
    def show(toggle: bool):
        label.setVisible(toggle)
        textbox.setVisible(toggle)

    for tup in zip(frame.widget_pairs, [cur.char, cur.phrase]):
        label, textbox = tup[0][0], tup[0][1]
        if tup[1] is not None:
            header = tup[1].hanzi
            meaning = tup[1].meaning
            label.setText(header)
            textbox.setText(meaning)
            show(True)
        else:
            show(False)


def __update_hint_label(frame: PinyinInput, cur: Current) -> None:
    hanzi = cur.char.hanzi if cur.char is not None else ''
    frame.hint.setText(hanzi)


def update_text(*args: tuple):
    for arg in args:
        if isinstance(arg[0], Body_UI):
            __update_body_label(arg[0], arg[1])
        elif isinstance(arg[0], SideColumn):
            __update_side_col(arg[0], arg[1])
        elif isinstance(arg[0], PinyinInput):
            __update_hint_label(arg[0], arg[1])
