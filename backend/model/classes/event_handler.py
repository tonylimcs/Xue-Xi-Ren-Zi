from PySide6.QtWidgets import QWidget

from backend.engine.classes.user import User
from backend.engine.constants import keys

from backend.model.constants.event_types import *
from backend.model.classes.body import Body
from backend.model.classes.current import Current
from backend.model import gui_controller as gui_ctrl

import re


class EventHandler:
    _body = Body()
    _cur = Current()
    _user = User()

    def init_gui(self, widget: QWidget) -> None:
        gui_ctrl.update((widget.body, self._body),
                        (widget.pinyin_input, self._cur))

    def user_input(self, widget: QWidget) -> None:
        if self._cur.char is None:
            return

        user_input = widget.pinyin_input.line_edit.text()
        print(f'[INPUT] "{user_input}"')

        def is_correct(input_: str, pinyin_: str):
            if len(input_) > 0 and not re.match(r'\d', input_[-1]):
                input_ += '5'
            return input_ == pinyin_

        hanzi = self._cur.char.hanzi
        pinyin = self._cur.char.pinyin
        correct = is_correct(user_input, pinyin)

        def update_user():
            # Update counter
            self._user.update_counter(hanzi, pinyin,
                                      correct=correct)

            # Update current character
            counter = self._user.get_counter(hanzi, pinyin)
            if counter == 0:
                self._cur.char.status = keys.LEARNED

        def update_body():
            self._body.update_answer(hanzi, pinyin,
                                     correct=correct)

            if self._cur.char.status == keys.LEARNED:
                self._body.update_to_learned(hanzi)

            self._cur.update_cur()

            self._body.update_highlight(self._cur.char)

        update_user()
        update_body()

        gui_ctrl.update((widget.body, self._body),
                        (widget.pinyin_input, self._cur))

    def handle(self, widget: QWidget, event: str) -> None:
        if event == GUI_INIT:
            print(f"[EVENT] {GUI_INIT}")
            self.init_gui(widget)
        elif event == USER_INPUT:
            self.user_input(widget)
