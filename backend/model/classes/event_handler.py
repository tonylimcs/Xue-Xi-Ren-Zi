from PySide6.QtWidgets import QWidget

from backend.engine.classes.user import User
from backend.engine.constants import keys

from backend.model.constants.event_types import *
from backend.model.classes.parsed import Parsed
from backend.model.classes.body import Body
from backend.model.classes.current import Current
from backend.model import gui_controller as gui_ctrl

import re


class EventHandler:
    _user = User()

    @staticmethod
    def update_text(parent: QWidget) -> None:
        print("[GUI UPDATE] Body text and hint...")
        gui_ctrl.update_text((parent.body, Body()),
                             (parent.side_col, Current()),
                             (parent.pinyin_input, Current()))

    def user_input(self, parent: QWidget) -> None:
        body = Body()
        cur = Current()

        if cur.char is None:
            return

        user_input = parent.pinyin_input.line_edit.text()
        print(f'[INPUT] "{user_input}"')

        def is_correct(input_: str, pinyin_: str):
            if len(input_) > 0 and not re.match(r'\d', input_[-1]):
                input_ += '5'
            return input_ == pinyin_

        hanzi = cur.char.hanzi
        pinyin = cur.char.pinyin
        correct = is_correct(user_input, pinyin)

        def update_user():
            # Update counter
            self._user.update_counter(hanzi, pinyin,
                                      correct=correct)

            # Update current character
            counter = self._user.get_counter(hanzi, pinyin)
            if counter == 0:
                cur.char.status = keys.LEARNED

        def update_body():
            body.update_answer(hanzi, pinyin,
                               correct=correct)

            if cur.char.status == keys.LEARNED:
                body.update_to_learned(hanzi)

            cur.update_cur()

            body.update_highlight(cur.char)

        update_user()
        update_body()

        self.update_text(parent)

    def finished(self, parent: QWidget) -> None:
        self._user.update_articles(Parsed().article_path)
        self._user.save_user()

        # TODO: Do something here, e.g. show a 'next' button
        #  to display next recommended article.
        # Parsed().update('articles/2.txt')
        # self.update_text(parent)

    def handle(self, parent: QWidget, event: str) -> None:
        if event == GUI_INIT:
            print(f"\n[EVENT] {GUI_INIT}")
            self.update_text(parent)
        elif event == USER_INPUT:
            print(f"\n[EVENT] {USER_INPUT}")
            self.user_input(parent)
        elif event == FINISHED:
            print(f"\n[EVENT] {FINISHED}")
            self.finished(parent)
            return  # Prevent endless recursions

        if Current().char is None:
            self.handle(parent, event=FINISHED)
