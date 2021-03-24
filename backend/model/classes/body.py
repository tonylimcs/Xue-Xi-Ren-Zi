from backend.engine.classes.singleton_meta import SingletonMeta
from backend.engine.classes.zh_entity import ZHEntity, Phrase, Character

from backend.model.classes.parsed import Parsed
from backend.model.txt2html import *


class Body(metaclass=SingletonMeta):
    _parsed = Parsed()

    def __init__(self):
        self._body_html = self.__init_body_html()

    def __repr__(self):
        return f"{self.__class__.__name__}"

    @property
    def body_html(self):
        return self._body_html

    def __init_body_html(self) -> str:
        """
        Convert parsed lines into a string of HTML format
        for the body text to be displayed on the GUI.
        :return: a string of HTML format
        """
        html_str = ''
        is_first = True
        unseen_idx = self._parsed.unseen
        for i, e in enumerate(self._parsed.parsed):
            string = e
            if isinstance(e, ZHEntity):
                chars = []
                if isinstance(e, Phrase):
                    chars += e.chars
                if isinstance(e, Character):
                    chars.append(e)

                strings = []
                for j, ch in enumerate(chars):
                    wrapped_str = ch.hanzi
                    idx = (i, j)
                    if idx in unseen_idx:
                        # Show pinyin for 'unseen' hanzi
                        wrapped_str = show_pinyin(ch.hanzi, ch.pinyin)
                        wrapped_str = color_code(wrapped_str, status=keys.UNSEEN)
                    elif ch.status == keys.LEARNING:
                        if is_first:
                            # Highlight the first 'learning' hanzi
                            wrapped_str = highlight_hanzi(ch.hanzi)
                            is_first = False    # Update flag

                    if idx not in unseen_idx:
                        wrapped_str = color_code(wrapped_str, status=ch.status)

                    strings.append(wrapped_str)
                string = ''.join(strings)
            elif e == '\n\n':
                # Convert to HTML tags
                string = '<br><br>'
            html_str += string
        return html_str

    def update_highlight(self, char: Character) -> None:
        if char is None:
            return

        original = color_code(char.hanzi, status=keys.LEARNING)

        highlighted_hanzi = highlight_hanzi(char.hanzi)
        updated = color_code(highlighted_hanzi, status=keys.LEARNING)

        self._body_html = self.body_html.replace(original, updated, 1)

    def update_answer(self, hanzi: str, pinyin: str, correct: bool) -> None:
        original = highlight_hanzi(hanzi)
        original = color_code(original, status=keys.LEARNING)

        updated = hanzi
        if not correct:
            updated = show_pinyin(hanzi, pinyin)
        result = keys.CORRECT if correct else keys.WRONG
        updated = color_code(updated, status=result)

        self._body_html = self.body_html.replace(original, updated, 1)

    def update_to_learned(self, hanzi: str) -> None:
        original = color_code(hanzi, status=keys.LEARNING)
        self._body_html = self.body_html.replace(original, hanzi)
